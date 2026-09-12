// Package apisio is a client for the apis.io API catalog.
//
// Deliberately small, and deliberately the same shape as the Python and JavaScript clients beside
// it: the operation bindings in operations.go are GENERATED from the OpenAPI documents apis.io
// publishes, by the same generator, so the three cannot drift from each other or from the contract.
//
// Three things this handles that a bare http.Get does not, and they are why a client library is
// worth having for this API rather than a thin wrapper:
//
//  1. 401 AND 402 MEAN DIFFERENT THINGS. A 401 says "you have not authenticated" and carries an
//     RFC 9728 challenge naming the resource-metadata document to bootstrap from. A 402 says "you
//     are authenticated and this costs more" and names the plan. Collapsing them is the most
//     common way an agent gets stuck here.
//  2. THE CHALLENGE DOES NOT ARRIVE UNDER ITS STANDARD NAME. API Gateway reserves
//     WWW-Authenticate and renames it; the value arrives as x-auth-challenge (and
//     x-amzn-remapped-www-authenticate). ResourceMetadata reads all three.
//  3. RATE-LIMIT STATE IS IN RESPONSE HEADERS, not the body, and is what you back off on.
//
// Standard library only.
package apisio

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"regexp"
	"strconv"
	"strings"
	"time"
)

const (
	DefaultBaseURL = "https://apis.io/api/v1"
	userAgent      = "apisio-go/0.1.0 (+https://apis.io)"
)

// APIError is any non-2xx answer. It carries the parsed body, because this API always explains itself.
type APIError struct {
	Status  int
	Body    map[string]any
	Headers http.Header
	URL     string
}

func (e *APIError) Error() string {
	return fmt.Sprintf("%d %v: %v", e.Status, e.Body["error"], e.Body["detail"])
}

// Code is the machine-readable `error` field, e.g. "upgrade_required", "not_purchasable".
func (e *APIError) Code() string {
	s, _ := e.Body["error"].(string)
	return s
}

// Unauthenticated is a 401: you have no credential. NOT a paywall — the challenge says how to get
// one. An agent that has never authenticated should read ResourceMetadata, fetch that document and
// register. See RFC 9728.
type Unauthenticated struct{ *APIError }

func (e *Unauthenticated) challenge() string {
	for _, n := range []string{"Www-Authenticate", "X-Auth-Challenge", "X-Amzn-Remapped-Www-Authenticate"} {
		if v := e.Headers.Get(n); v != "" {
			return v
		}
	}
	return ""
}

var reResourceMetadata = regexp.MustCompile(`resource_metadata="([^"]+)"`)
var reScope = regexp.MustCompile(`scope="([^"]+)"`)

// ResourceMetadata is the RFC 9728 metadata URL, from whichever header survived the hop.
func (e *Unauthenticated) ResourceMetadata() string {
	if m := reResourceMetadata.FindStringSubmatch(e.challenge()); m != nil {
		return m[1]
	}
	return ""
}

func (e *Unauthenticated) Scope() string {
	if m := reScope.FindStringSubmatch(e.challenge()); m != nil {
		return m[1]
	}
	return ""
}

// PaymentRequired is a 402: authenticated, and this resource needs a higher plan.
type PaymentRequired struct{ *APIError }

func (e *PaymentRequired) Tier() string     { s, _ := e.Body["tier"].(string); return s }
func (e *PaymentRequired) PlansURL() string { s, _ := e.Body["plans"].(string); return s }

// RateLimited is a 429. RetryAfter is seconds, when the server said.
type RateLimited struct{ *APIError }

func (e *RateLimited) RetryAfter() float64 {
	v, err := strconv.ParseFloat(e.Headers.Get("Retry-After"), 64)
	if err != nil {
		return 0
	}
	return v
}

// NotFound is a 404: no such provider, api, tag or dataset.
type NotFound struct{ *APIError }

// RateLimit is what the response headers said about your remaining budget.
type RateLimit struct {
	Tier   string
	Limit  int
	Window int
	Policy string
}

func rateLimitOf(h http.Header) RateLimit {
	atoi := func(s string) int { n, _ := strconv.Atoi(s); return n }
	return RateLimit{
		Tier:   h.Get("X-Ratelimit-Tier"),
		Limit:  atoi(h.Get("X-Ratelimit-Limit")),
		Window: atoi(h.Get("X-Ratelimit-Window")),
		Policy: h.Get("Ratelimit-Policy"),
	}
}

// Meta is the pagination block on a collection response.
type Meta struct {
	Total int `json:"total"`
	Page  int `json:"page"`
	Limit int `json:"limit"`
	Pages int `json:"pages"`
}

// Page is a page of results plus the meta block saying where you are.
type Page struct {
	Data      []map[string]any
	Meta      Meta
	RateLimit RateLimit
	Raw       map[string]any
}

// Client is a client for apis.io. The zero value is not usable; call New.
//
// Most of the catalog is free and needs no key. Anything that synthesises across it — ratings,
// cohorts, insights — needs a plan, and returns a *PaymentRequired naming which one.
type Client struct {
	APIKey        string
	BaseURL       string
	HTTP          *http.Client
	MaxRetries    int
	LastRateLimit RateLimit
}

type Option func(*Client)

func WithAPIKey(k string) Option      { return func(c *Client) { c.APIKey = k } }
func WithBaseURL(u string) Option     { return func(c *Client) { c.BaseURL = strings.TrimRight(u, "/") } }
func WithHTTPClient(h *http.Client) Option { return func(c *Client) { c.HTTP = h } }

func New(opts ...Option) *Client {
	c := &Client{
		BaseURL:    DefaultBaseURL,
		HTTP:       &http.Client{Timeout: 30 * time.Second},
		MaxRetries: 2,
	}
	for _, o := range opts {
		o(c)
	}
	return c
}

func errorFor(status int, body map[string]any, h http.Header, u string) error {
	base := &APIError{Status: status, Body: body, Headers: h, URL: u}
	switch status {
	case http.StatusUnauthorized:
		return &Unauthenticated{base}
	case http.StatusPaymentRequired:
		return &PaymentRequired{base}
	case http.StatusNotFound:
		return &NotFound{base}
	case http.StatusTooManyRequests:
		return &RateLimited{base}
	}
	return base
}

// Request makes one call. It returns the parsed body, or a typed error on non-2xx.
func (c *Client) Request(ctx context.Context, method, path string, params map[string]any, payload any) (any, error) {
	q := url.Values{}
	for k, v := range params {
		if v == nil {
			continue
		}
		q.Set(k, fmt.Sprintf("%v", v))
	}
	u := c.BaseURL + "/" + strings.TrimLeft(path, "/")
	if s := q.Encode(); s != "" {
		u += "?" + s
	}

	var raw []byte
	if payload != nil {
		var err error
		if raw, err = json.Marshal(payload); err != nil {
			return nil, err
		}
	}

	for attempt := 0; ; attempt++ {
		var rdr io.Reader
		if raw != nil {
			rdr = bytes.NewReader(raw)
		}
		req, err := http.NewRequestWithContext(ctx, strings.ToUpper(method), u, rdr)
		if err != nil {
			return nil, err
		}
		req.Header.Set("Accept", "application/json")
		req.Header.Set("User-Agent", userAgent)
		// Omit the header entirely for the keyless free tier — an empty or wrong key is an
		// `invalid_key` 401, which reads like a bug and is not one.
		if c.APIKey != "" {
			req.Header.Set("X-Api-Key", c.APIKey)
		}
		if raw != nil {
			req.Header.Set("Content-Type", "application/json")
		}

		res, err := c.HTTP.Do(req)
		if err != nil {
			if attempt < c.MaxRetries {
				time.Sleep(time.Duration(1<<attempt) * time.Second)
				continue
			}
			return nil, &APIError{Status: 0, Body: map[string]any{"error": "network", "detail": err.Error()}, URL: u}
		}

		b, _ := io.ReadAll(res.Body)
		res.Body.Close()
		c.LastRateLimit = rateLimitOf(res.Header)

		var body any
		if len(b) > 0 {
			if err := json.Unmarshal(b, &body); err != nil {
				body = map[string]any{"detail": string(b)}
			}
		}
		if res.StatusCode >= 200 && res.StatusCode < 300 {
			return body, nil
		}

		m, _ := body.(map[string]any)
		if m == nil {
			m = map[string]any{}
		}
		e := errorFor(res.StatusCode, m, res.Header, u)
		// Retry only what retrying can fix. A 402 will never become a 200 by asking again.
		if rl, ok := e.(*RateLimited); ok && attempt < c.MaxRetries {
			d := rl.RetryAfter()
			if d == 0 {
				d = float64(int(1) << attempt)
			}
			time.Sleep(time.Duration(d * float64(time.Second)))
			continue
		}
		if res.StatusCode >= 500 && attempt < c.MaxRetries {
			time.Sleep(time.Duration(1<<attempt) * time.Second)
			continue
		}
		return nil, e
	}
}

func (c *Client) Get(ctx context.Context, path string, params map[string]any) (any, error) {
	return c.Request(ctx, "GET", path, params, nil)
}

// GetPage calls a list endpoint and returns it as a Page. Collection responses are {meta, data}.
func (c *Client) GetPage(ctx context.Context, path string, params map[string]any) (*Page, error) {
	body, err := c.Get(ctx, path, params)
	if err != nil {
		return nil, err
	}
	p := &Page{RateLimit: c.LastRateLimit}
	m, ok := body.(map[string]any)
	if !ok {
		return p, nil
	}
	p.Raw = m
	if md, ok := m["meta"].(map[string]any); ok {
		b, _ := json.Marshal(md)
		_ = json.Unmarshal(b, &p.Meta)
	}
	if rows, ok := m["data"].([]any); ok {
		for _, r := range rows {
			if rm, ok := r.(map[string]any); ok {
				p.Data = append(p.Data, rm)
			}
		}
	}
	return p, nil
}
