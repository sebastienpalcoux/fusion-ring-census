.PHONY: test smoke verify docs site
PYTHON ?= python3
test:
	$(PYTHON) -m unittest discover -s tests -v
smoke:
	$(PYTHON) scripts/smoke_test.py --out runs/smoke
verify:
	$(PYTHON) scripts/check_release.py --full --out runs/full-verification.json
docs:
	$(PYTHON) scripts/refresh_documentation.py
	$(PYTHON) scripts/build_manuscripts.py --compile
site:
	$(PYTHON) scripts/build_site.py
