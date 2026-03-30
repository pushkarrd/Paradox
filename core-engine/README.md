Core Engine API Integration

This branch now includes a lightweight API wrapper for the core engine.

Run steps
1. Open terminal in core-engine.
2. Install dependencies:
   pip install -r requirements.txt
3. Start API:
   python api_server.py

Endpoints
- GET /health
- POST /api/validate

POST body (frontend contract)
{
  "source": "samples/clean.c",
  "suspect": "samples/fake_compiler.py",
  "trusted": "gcc"
}

Notes
- If suspect points to a .py compiler script, the API automatically runs it with the active Python interpreter.
- Relative paths resolve from the core-engine directory.
- Response is shaped to match the dashboard fields:
  verdict, trust_score, crack_type, severity, diffs, actions, report.
