from openai import OpenAI
from rich.console import Console
from rich.panel import Panel

from shared.settings import get_settings

console = Console()
settings = get_settings()
selected_model=settings.nv_gpt_120

def main() -> None:
    client = OpenAI(base_url=settings.nvidia_url,
        api_key=settings.nvidia_api_key)

    console.print(
        Panel.fit(
            "[bold cyan] AI Engineering Assistnat[/bold cyan]"
        )
    )
    console.print(f"[bold]Provider :[/bold] OpenAI")
    console.print(f"[bold]Model    :[/bold] {selected_model}")
    console.print()

    prompt = console.input("[bold green]You > [/bold green]")

    response = client.responses.create(
        model=selected_model,
        input=prompt
    )
    usage =response.usage
    # console.print(response)
    console.print(f"[bold cyan]AI > {response.output_text}[/bold cyan]")
    console.print(f"[bold yellow]Input Tokens > {usage.input_tokens} || Output Tokens > {usage.output_tokens} || Total Tokens > {usage.total_tokens}")
    # console.print(response.output_text)

if __name__ == "__main__":
    main()