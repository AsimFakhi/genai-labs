import json
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

from shared.settings import get_settings
from foundations.module_05_structured_outputs.prompts import SYSTEM_PROMPT
from foundations.module_05_structured_outputs.schemas import SnowFlakeMetadata

settings = get_settings()
console = Console()
client = OpenAI(base_url=settings.nvidia_url,
                api_key=settings.nvidia_api_key)
model_use = settings.nv_gpt_20

def print_header():
    terminal_width = console.size.width
    padding = 2
    panel_width = console.size.width - (padding*2)
    console.print(
        Panel(
            Align.center(
                "\n[bold cyan]Structured Output Playground[/bold cyan]\n"
                f"[bold]Provider[/bold] : OpenRouter\n"
                f"[bold]Model[/bold]    : {model_use}",
            ),width=panel_width
        )
    )
    console.print()

def get_power_query():
    console.print("[bold green]Paste Power Query below." )
    console.print("[dim]Type END on a new line to finish.[/dim]\n")
    lines = []

    while True:
        line = input()
        if line.lower() in ("exit", "quit", "cls"):
            return None
        if line.strip().upper() == "END":
            console.print(f"[bold cyan]\nQuery capture complete.Please wait while we proces the request...[/bold cyan]")
            break
        lines.append(line)
    return "\n".join(lines)
    
def extract_metadata(power_query:str):
    response = client.responses.parse(
        model=model_use,
        input=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":power_query}
        ],
        text_format=SnowFlakeMetadata,
    )

    return response.output_parsed, response.usage

def main():
    print_header()

    while True:
        power_query = get_power_query()
        if power_query is None:
            break
        

        try:
            meta_data, usage = extract_metadata(power_query)
        except Exception as ex:
            console.print(f"[red]Error:[/red] {ex}")
            continue
        console.rule("[bold green]Extracted Metadata")
        console.print(meta_data)
        console.rule("\n[bold cyan]JSON")
        console.print_json(
            json.dumps(
                meta_data.model_dump(), indent=4
            )
        )

        console.print(
            Panel(
                Align.center("[bold yellow]Token Usage"
                    f"[bold yellow]Input Tokens > {usage.input_tokens} "
                    f"|| Output Tokens > {usage.output_tokens} "
                    f"|| Total Tokens > {usage.total_tokens}[/bold yellow]"
                    ), style="yellow"
            )
        )
        console.print("\n\n")
if __name__=="__main__":
    main()


