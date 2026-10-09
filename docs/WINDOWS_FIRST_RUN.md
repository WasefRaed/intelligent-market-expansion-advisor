# First Run on Windows — Submission Candidate (2026-10-10)

1. Extract the **final submission ZIP** on your Desktop and open its `intelligent-market-expansion-advisor` directory in VS Code.
2. Open **Terminal → New Terminal** and run from the project root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m streamlit run app/ui.py
```

3. Open `http://localhost:8501` in a browser. **Location Explorer, Unit Economics, and Evidence & Methodology work without any Gemini API key.**
4. For AI chat only: copy `.env.example` to `.env`, edit the private `GOOGLE_API_KEY` and supported Gemini model settings, then restart Streamlit. You can alternatively copy your existing private `.env` **locally** from the earlier Phase 6 project. Never commit or upload `.env`.
5. If Gemini returns `429`, do not retry repeatedly. Check quota status offline with:

```powershell
.\.venv\Scripts\python.exe -m app.quota_guard status
```

The user's existing **Phase 6** local project had **72 passing tests** and successfully started Streamlit on 2026-10-10. This extracted submission candidate has identical application code plus updated documentation; its offline suite has also passed during packaging. See [`GITHUB_PUBLISHING.md`](GITHUB_PUBLISHING.md) to publish safely and [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md) to record the presentation.
