from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt

from shared.settings import get_settings
from foundations.module_04_prompt_eng.prompt_builder import PROMPTS

settings = get_settings()
console = Console()
client = OpenAI(base_url=settings.openrouter_url,
                api_key=settings.openrouter_api_key)
SHOW_PROMPT = False

def print_header():
    terminal_width = console.size.width
    padding = 2
    panel_width = console.size.width - (padding*2)
    console.print(
        Panel(
            Align.center(
                "\n[bold cyan]Prompt Engineering Playground[/bold cyan]\n"
                f"[bold]Provider[/bold] : OpenRouter\n"
                f"[bold]Model[/bold]    : {settings.free_router}",
                vertical="middle",
            )
        )
    )
    console.print()

def ask_llm(prompt:str):
    response = client.responses.create(
        model=settings.free_router,
        input=prompt,
    )
    return response.output_text, response.usage

def main():
    print_header()

    while True:
        question = console.input("[bold green]Question > [/bold green]")

        if question.lower() in ["exit", "quit", "cls"]:
            break

        input_tokens = 0
        output_toekns = 0
        total_tokens = 0

        console.print()
        for prompt_name, builder in PROMPTS.items():
            console.rule(f"[bold blue]{prompt_name}")
            prompt = builder(question)
            
            if SHOW_PROMPT:
                console.print("[bold magenta]Prompt Sent:[/bold magenta]")
                console.print(prompt)
                console.print()
            answer, usage = ask_llm(prompt=prompt)
            console.print(f"[bold cyan]AI > [/bold cyan]\n{answer}\n")
            console.print(f"\n[bold yellow]Tokens used with this prompt. [/bold yellow]")
            console.print(f"[bold yellow]Input Tokens> {usage.input_tokens} || Output Tokens > {usage.output_tokens} || Total Tokens > {usage.total_tokens}[/bold yellow]]\n")

            input_tokens += usage.input_tokens
            output_toekns += usage.output_tokens
            total_tokens +=usage.total_tokens

            console.print()

        console.rule("[bold green]Conversation Summary")

        console.print(
            f"[bold yellow]Input Tokens :[/bold yellow] {input_tokens}"
        )
        console.print(
            f"[bold yellow]Output Tokens:[/bold yellow] {output_toekns}"
        )
        console.print(
            f"[bold yellow]Total Tokens :[/bold yellow] {total_tokens}"
        )

        console.print()
if __name__=="__main__":
    main()