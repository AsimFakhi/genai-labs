# uv run python -m foundations.module_02_conversation_assistant.chatbot
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt
from rich.terminal_theme import MONOKAI

# console = Console(record=True)

from shared.settings import get_settings

settings = get_settings()

console = Console()
terminal_width = console.size.width
padding = 2 
panel_width = console.size.width - (padding * 2)

console.print(
    Panel(
        Align.center(
            "[bold cyan]Asim's AI Assistant[/bold cyan]\n"
            f"[bold]Provider[/bold] : OpenRouter\n"
            f"[bold]Model[/bold]    : {settings.nv_gpt_120}",
            vertical="middle",
        ),
        width=panel_width,
    )
)

# Initialize OpenAI SDK client
client = OpenAI(base_url=settings.nvidia_url,
                api_key=settings.nvidia_api_key)
# Stores the entire conversation history
conversation = []
input_tokens = 0
output_tokens = 0
total_tokens = 0

while True:

    prompt = Prompt.ask("[bold green]You[/bold green]")

    if prompt.lower() in {"exit", "quit","cls"}:
        break

    # Store the user's message
    conversation.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # Send the full conversation history
    response = client.responses.create(
        model=settings.nv_gpt_120,
        input=conversation,
    )

    answer = response.output_text

    # Store the assistant's reply
    conversation.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    
    if response:
        console.print(f"\n[bold cyan]AI >[/bold cyan] {answer}\n")
        usage =response.usage
        input_tokens = input_tokens + usage.input_tokens
        output_tokens = output_tokens + usage.output_tokens
        total_tokens = total_tokens + usage.total_tokens
        console.print("[tan]-[/tan]"*80)
    else:
        console.print(f"\n[bold cyan]AI >[/bold cyan] \n")

console.print("[yellow]-[/yellow]"*80)
console.print(f"\n[bold yellow]Tokens used in this conversation. [/bold yellow]")
console.print(f"[bold yellow]Input Tokens> {input_tokens} || Output Tokens > {output_tokens} || Total Tokens > {total_tokens}[/bold yellow]]\n")
# console.save_svg("example.svg", theme=MONOKAI)