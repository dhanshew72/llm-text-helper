# llm-text-helper
Upload a document and ask questions to answer about it.

## How to Run Locally
1. First, ensure you're running Python 3.11 or later.
2. Run `make dev-env` to create development environment.
3. Run `make run-local` to spin up the service and connect via `localhost:8000` to start using.


## Notes
- The UI doesn't display if a file is successfully uploaded, but if you don't see an error message it'll be fine.
- Expect queries to take about ~10 seconds to run.
- Everything is stored locally inside the repo directory.
