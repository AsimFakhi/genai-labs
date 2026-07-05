# uv run python -m foundations.module_06_tool_calling.main
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from pprint import pprint

from shared.settings import get_settings
from foundations.module_06_tool_calling.prompts import SYSTEM_PROMPT

settings = get_settings()
console = Console()

client = OpenAI(
    # base_url=settings.openrouter_url,
    api_key=settings.openai_api_key
)

MODEL = settings.gpt_nano

# Header
def print_header():
    console.print(
        Panel(
            Align.center(
                "[bold cyan] Module 06 - Tool Calling[/bold cyan]\n"
                f"Model : {MODEL}"
            )
        )
    )

# Actual DB Schema
# The LLM never sees this code.
# It only sees the tool description.
def get_database_schema():
    """
    Returns the database schema.
    """
    return """
    Table:
    costomers
    accounts
    transactions
    merchants
    transaction_types

    Relationships

    customer.customer_id -> accounts.customer_id

    accounts.account_id -> transaction.account_id
    
    merchant.merchat_id -> transaction.merchant_id

    transaction_types.transaction_type_id -> transaction.transaction_type_id
"""

# Register Tool
TOOLS = [
    {
        "type": "function",
        "name": "get_database_schema",
        "description": "Returns the SQLite database schema including tables and relationships.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

def main():
    print_header()
    while True:
        question = input("\nYou > ")
        if question.lower() in ("exit", "quit", "cls"):
            break


        response = client.responses.create(
            model=MODEL,
            input=[
                {"role":"system", "content": SYSTEM_PROMPT},
                {"role":"user", "content": question}
            ],
            tools=TOOLS
        )

        console.rule("Raw Response")
        console.print(response.model_dump())

        function_calls = [
            item 
            for item in response.output
            if item.type == "function_call"
        ]

        if not function_calls:
            console.print(f"\n[bold green]AI > {response.output_text}[/bold green]")
            continue

        for call in function_calls:
            if call.name == "get_database_schema":
                tool_result = get_database_schema()
                final_response = client.responses.create(
                    model=MODEL,
                    previous_response_id = response.id,
                    input=[
                        {
                            "type":"function_call_output", 
                            "call_id":call.call_id, 
                            "output":tool_result
                        }
                    ],
                )

                console.print("\n")
                console.print(
    f"[bold green]AI > {final_response.output_text}[/bold green]"
)

if __name__ == "__main__":
    main()