# Publish the Final Project to GitHub — Windows Walkthrough

This folder is a **submission candidate**, not an already published repository. You must create the GitHub repository and video link yourself. The downloaded ZIP intentionally contains **no `.env`, `.venv`, `.runtime`, or API credentials**.

## 1. Confirm the release candidate works

Extract the release ZIP to the Desktop. In **VS Code → File → Open Folder**, open `intelligent-market-expansion-advisor` from the extracted location. In its PowerShell terminal:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
```

If you want live AI in this **new** folder, copy only your existing local `.env` from Phase 6, or create it from `.env.example`. `.env` must remain private. The offline tests and non-AI tabs do not require a key. Record the test results for your submission.

## 2. Ensure Git is available

In the same VS Code terminal:

```powershell
git --version
```

If Git is missing, install Git for Windows from https://git-scm.com/downloads/win and restart VS Code. GitHub Desktop (https://desktop.github.com/) is another option if you prefer not to use terminal commands.

## 3. Create a new empty repository

Sign in to https://github.com/new and create a repository named, for example, `intelligent-market-expansion-advisor`. Choose visibility per assignment rules. **Do not** initialize it with a GitHub README, license, or `.gitignore` because those files are already in this project.

## 4. Stage and check files locally

From the project root:

```powershell
git init
git add .
git status --short
```

Inspect the file list carefully. `README.md`, `app/`, `tests/`, `docs/`, `evals/`, `data/`, `.env.example` and `.github/workflows/tests.yml` **should** appear. The following **must not** appear: `.env`, `.venv/`, `.runtime/`, actual Gemini keys, or private diagnostics. `git check-ignore .env` can confirm the key file is ignored (if one exists).

If `.env` appears as a staged file, immediately unstage it with `git rm --cached .env`, check `.gitignore`, and do **not** push until resolved.

## 5. Commit and publish

```powershell
git commit -m "Prepare UAE market expansion advisor submission"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/intelligent-market-expansion-advisor.git
git push -u origin main
```

Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username. If `git commit` asks for an identity, set your chosen public Git commit identity with `git config --global user.name "..."` and `git config --global user.email "..."`, then retry. If `origin` already exists, use `git remote -v` to inspect it before changing anything. GitHub may require browser sign-in, Git Credential Manager, or an approved authentication flow; GitHub account passwords are not accepted as normal HTTPS Git credentials.

## 6. Validate what reviewers will see

Open the GitHub repository URL in a browser. Check README formatting, all project files, evaluation links, source data notes, and that `.env` is **not** present. GitHub Actions (if enabled for the repo) will run the **offline** unit tests without a Gemini secret. Its result is a supplementary check; your locally verified Windows tests remain the source of the recorded 72/72 result.

## 7. Record and share the demo

Use [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md), aim for 2–3 minutes, and upload the recording using the method accepted by the assignment (e.g., an unlisted video link when permitted). Test that reviewers can open the link without requesting access.

## Submission entries

- **Repository URL:** the actual published GitHub URL.
- **Demo video URL:** your accessible recording link.
- **Summary:** "Python/Agno five-specialist UAE restaurant expansion advisory chatbot with Streamlit, deterministic scenario tools, bounded official reference notes, manual business evaluations, and quota-aware Gemini fallback."
- **Disclosure:** link to [`AI_TOOL_DISCLOSURE.md`](AI_TOOL_DISCLOSURE.md).
- **Known limitations:** link to [`COST_AND_LIMITATIONS.md`](COST_AND_LIMITATIONS.md).
