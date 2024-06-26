ACTIVATE_VENV=. .venv/bin/activate

dev-env: clean
	python3 -m venv .venv
	$(ACTIVATE_VENV); pip3 install -r requirements.txt

clean:
	rm -rf .venv

run-local:
	$(ACTIVATE_VENV); fastapi dev src/routes.py
