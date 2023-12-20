.PHONY: venv
venv:
	python -m venv .venv
	. .venv/bin/activate; pip --require-virtualenv install -r requirements.txt
	. .venv/bin/activate; pip --require-virtualenv check


.PHONY: deploy
deploy:
	rm -rf ./dist
	. .venv/bin/activate; python -m build
	. .venv/bin/activate; python -m twine upload ./dist/*

.PHONY: requirements.txt
requirements.txt:
	. .venv/bin/activate; pip freeze > requirements.txt
