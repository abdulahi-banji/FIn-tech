# Money Brain

A Fintech Club dashboard built with Python and Streamlit. All data is fictional.

## Run locally

Use Python 3.11 or newer (Codespaces uses 3.12).

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

In Codespaces, dependencies install automatically. Run `streamlit run app.py`
and open port 8501.

## October 23 deliverables

- [Team plan, five features, and five questions](docs/plan.md)
- [Main-screen sketch](docs/main-screen.md)
- [60-second share-out](docs/share-out.md)
- Runnable demo with balances, transactions, spending filters, and purchase alerts

Team name and role assignments still need team confirmation. The team must also
validate the app and deliver the share-out.

## Roadmap

| Date | Session |
| --- | --- |
| Oct 23 | Plan and set up |
| Oct 30 | Connect Plaid Sandbox |
| Nov 6 | Add an AI assistant |
| Nov 13 | Security review |
| Nov 20 | Demo night |

The question panel currently calculates answers from sample data. Bank connections
and AI are future work. Do not enter real financial records or credentials.
Local `.env` files and `.streamlit/secrets.toml` are ignored by Git.

## Verify

```sh
python -m unittest discover -s tests -v
python -m pip check
```

The tests exercise spending totals, all five answers, category/month filters,
empty results, and alert thresholds with Streamlit's app runner.
