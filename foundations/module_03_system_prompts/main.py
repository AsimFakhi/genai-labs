from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.prompt import Prompt

from shared.settings import get_settings
from foundations.module_03_system_prompts.prompts import TEACHER, PIRATE, INTERVIEWER, CONCISE

console = Console()
settings = get_settings()


# Initialize the OpenAI Client
client = OpenAI(base_url=settings.openrouter_url,
                api_key=settings.openrouter_api_key)

# Available system prompts
PROMPTS = {
    "1": ("Teacher", TEACHER),
    "2": ("Pirate", PIRATE),
    "3": ("Interviewer", INTERVIEWER),
    "4": ("Concise Assistant", CONCISE)
}

console.print(f"[bold cyan]=== Module 03: System Prompts ===[/bold cyan]\n")

console.print("Chose an assitant persona:\n")
for key, (name, _) in PROMPTS.items():
    console.print(f"{key}. {name}")

choice = input("\nEnter your choice (1-4):").strip()

if choice not in PROMPTS:
    console.print("[bold red]Invalid choice! Exiting..[/bold red]")
    exit()

assitant_name, system_prompt = PROMPTS[choice]
console.print(f"\n[bold green]You selected:[/bold green] {assitant_name}\n")

# The conversation always begins with the system message
conversation = [
    {
        "role":"system",
        "content":system_prompt
    }
]

# Token counter
input_tokens = 0
output_tokens = 0
total_tokens = 0

while True:
    user_input = Prompt.ask("[bold green]You > [/bold green]")

    if user_input.lower() in ["exit", "cls", "quit"]:
        break
    # Add user message
    conversation.append(
        {
            "role":"user",
            "content":user_input
        }
    )
    response = client.chat.completions.create(
        model=settings.free_router,
        messages=conversation
    )
    answer = response.choices[0].message.content

    # Display response
    console.print(f"\n[bold cyan]{assitant_name} > [/bold cyan]{answer}\n")

    # Save assistant response
    conversation.append(
        {
            "role":"assitant",
            "content":answer
        }
    )

    # Update token usage
    usage = response.usage
    input_tokens += usage.prompt_tokens
    output_tokens += usage.completion_tokens
    total_tokens += usage.total_tokens

    console.print("-"*60)

console.print("[yellow]-[/yellow]"*80)
console.print(f"\n[bold yellow]Tokens used in this conversation. [/bold yellow]")
console.print(f"[bold yellow]Input Tokens> {input_tokens} || Output Tokens > {output_tokens} || Total Tokens > {total_tokens}[/bold yellow]]\n")
