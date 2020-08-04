HOST=127.0.0.1

install:
	pip install requirements.txt

update-requirements: install
	pip freeze > requirements.txt

cclean: cclean
	black project_vulcan.py
	isort project_vulcan.py
	flake8 project_vulcan.py

run: run
	streamlit run project_vulcan.py

