from openai import OpenAI
from rich.console import Console
from rich.panel import Panel

from shared.settings import get_settings

console = Console()
settings = get_settings()

def main() -> None:
    # Stores the entire conversation history
    conversation = [] 
    input_tokens = 0
    output_tokens = 0
    total_tokens = 0
    client = OpenAI(api_key=settings.openai_api_key)

    console.print(
        Panel.fit(
            "[bold cyan] AI Engineering Assistnat[/bold cyan]"
        )
    )
    console.print(f"[bold]Provider :[/bold] OpenAI")
    console.print(f"[bold]Model    :[/bold] {settings.gpt_nano}")
    console.print()
    while True:
        prompt = console.input("[bold green]You > [/bold green]")

        if prompt.lower() in {"exit", "quite"}:
            break
        # Before calling OpenAI, append the user's message.
        conversation.append(
            {
                "role":"user",
                "content":prompt
            }
        )
        # Send the full conversation history
        response = client.responses.create(
            model=settings.gpt_nano,
            input=conversation
        )
        answer = response.output_text
        # Store the assistant's reply
        conversation.append(
            {
                "role":"assistant",
                "content":answer
            }
        )
        usage =response.usage
        # console.print(response)
        console.print(f"[bold cyan]AI > {answer}[/bold cyan]")
        input_tokens = input_tokens + usage.input_tokens
        output_tokens = output_tokens + usage.output_tokens
        total_tokens = total_tokens + usage.total_tokens
        console.print("-"*30)

    console.print(f"\n[bold yellow]Tokens used in this conversation. [/bold yellow]")
    console.print(f"[bold yellow]Input Tokens> {input_tokens} || Output Tokens > {output_tokens} || Total Tokens > {total_tokens}[/bold yellow]]\n")

if __name__ == "__main__":
    main()