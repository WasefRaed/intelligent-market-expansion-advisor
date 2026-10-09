from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_requirements_and_example_are_gemini_focused():
    req = (ROOT / 'requirements.txt').read_text()
    env = (ROOT / '.env.example').read_text()
    assert 'google-genai' in req
    assert 'agno==2.9.0' in req
    assert 'GOOGLE_API_KEY=' in env
    assert 'ENABLE_LIVE_RESEARCH=' in env
    assert 'OPENAI_API_KEY=' not in env


def test_gitignore_protects_secrets():
    ignored = (ROOT / '.gitignore').read_text().splitlines()
    assert '.env' in ignored
    assert '.venv/' in ignored
