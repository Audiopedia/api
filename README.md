# Audiopedia API

View the docs here: https://audiopedia-t4sg.github.io/api-docs/

---
Local installation instructions:
- Use Python 3.6.5 
    - Recommended: use `virtualenv -p ~/.pyenv/shims/python3.6 ~/.virtualenvs/api` to create the virtual environment (must install `virtualenv` and `pyenv` and run `pyenv install -v 3.6.5` for this to work)
    - `source ~/.virtualenvs/api/bin/activate` to activate the virtual environment
    - `deactivate` to deactivate
- Add `secure.py` (not included in GitHub repo) to `audiopedia/audiopedia` directory
- From the `audiopedia/` directory run `pip install -r requirements.txt`
- From the `audiopedia/` directory run `python manage.py migrate`

To run the project locally, run `python manage.py runserver` and navigate to http://localhost/graphql to interact with the GraphiQL explorer. See documentation for example queries/mutations.
