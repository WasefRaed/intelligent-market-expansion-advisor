from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from app.advisory_service import run_advice
from app.config import ENABLE_LIVE_RESEARCH
from app.runtime import friendly_provider_error

console = Console()

WELCOME = """# Intelligent Market Expansion Advisor — UAE

**Client:** Jordanian meaty-pizza & kebab restaurant  
**Markets:** Dubai + Abu Dhabi  
**Mode:** Multi-agent executive advisory

Ask questions such as:
- Which Dubai area should we open first and why?
- Compare JLT vs Al Reem Island for our first branch.
- What should our UAE menu and price architecture look like?
- Who are our closest competitors and how should we position against them?
- Build a 90-day launch plan for Abu Dhabi.
- What operational and licensing risks should management plan for?

Type `exit` to quit.
"""

def main():
    console.print(Panel(Markdown(WELCOME), title="UAE Expansion Advisor", expand=False))
    if not ENABLE_LIVE_RESEARCH:
        console.print("[yellow]Live Google Search is OFF.[/yellow] Snapshot-based guidance only. "
                      "Set ENABLE_LIVE_RESEARCH=true in .env to enable it (uses API quota).")
    while True:
        question = Prompt.ask("\n[bold cyan]Executive question[/bold cyan]")
        if question.strip().lower() in {"exit", "quit", "q"}:
            console.print("Goodbye.")
            break
        if not question.strip():
            continue
        try:
            # Shared entrypoint applies deterministic finance and the local
            # Gemini cooldown guard to CLI as well as Streamlit.
            content = run_advice(question, mode="team")
            console.print("\n" + "=" * 90)
            console.print(Markdown(content))
        except Exception as exc:
            message = str(exc)
            classified = friendly_provider_error(message)
            if classified:
                console.print(f"[red]{classified}[/red]")
            elif "429" in message or "RESOURCE_EXHAUSTED" in message:
                console.print("[red]Gemini quota limit reached (429).[/red] Check "
                              "https://ai.dev/rate-limit ; disable live research or "
                              "retry after the applicable quota resets. Changing model "
                              "may not help if limits are shared by project.")
            elif "503" in message or "UNAVAILABLE" in message:
                console.print("[red]Gemini temporarily unavailable (503).[/red] "
                              "Configured retries/fallback were attempted; try later.")
            else:
                console.print(f"[red]Advisor error:[/red] {exc}")
                console.print("Check GOOGLE_API_KEY, GEMINI_MODEL and your connection.")

if __name__ == "__main__":
    main()
