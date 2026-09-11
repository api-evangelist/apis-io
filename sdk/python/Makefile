.PHONY: generate check test

# Re-derive the operation bindings from the OpenAPI documents apis.io publishes.
generate:
	python3 generate.py

# Fails if the committed bindings no longer match the published contract. Run in CI.
check:
	python3 generate.py --check

test:
	python3 -m unittest discover -s tests -v
