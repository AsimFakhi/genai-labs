# uv run python -m foundations.module_06_tool_calling.main
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from pprint import pprint
import json

from shared.settings import get_settings
from foundations.module_06_tool_calling.prompts import SYSTEM_PROMPT
from foundations.module_06_tool_calling.tools import TOOLS, TOOLS_MAP


settings = get_settings()
console = Console()

client = OpenAI(
    # base_url=settings.openrouter_url,
    api_key=settings.openai_api_key
)

MODEL = settings.gpt_nano

# Header
def print_header():
    terminal_width = console.size.width
    console.print(
        Panel(
            Align.center(
                "[bold cyan] Module 06 - Tool Calling[/bold cyan]\n"
                f"Model : {MODEL}"
            ),width=terminal_width-4
        )
    )

# ------------------------------------------------------------------
# Tool Execution
# ------------------------------------------------------------------
def handle_tool_calls(response):
    """
    Execute every tool requested by the model.
    Parameters
    ----------
    response
        The response object returned by OpenAI

    Returns
    -----------
    Response 
        Final response after tool execution
    """
    # Find every tool call inside the response
    function_calls = [
        item
         for item in response.output
         if item.type == "function_call"
    ]
    # console.print("-"*80)
    # console.print(f"\n[bold medium_orchid1]Funtions call returned by LLM:> \n[/bold medium_orchid1]")
    # pprint(function_calls)
    if not function_calls:
        return response
    
    # ── Phase 1: Execute ALL tools ─────────────────────────
    tool_outputs = []
    for call in function_calls:
        console.print(f"\n[yellow bold]Calling Tool :> [/yellow bold]{call.name}")
        # Find matching python fucntion
        tool =TOOLS_MAP.get(call.name)

        if tool is None:
            console.print(f"[red]unknown tool : {call.name}[/red]")
            continue

        # Converts JSON to python dict
        arguments = json.loads(call.arguments)
        # xecute tool.
        result = tool(**arguments)
        console.print("-"*80,{result},"-"*80, sep="\n")
        tool_outputs.append(
            {
                "type":"function_call_output", 
                "call_id":call.call_id, 
                "output":result
            }
        )
        # pprint(f"Tools Output :>\n {tool_outputs}")
    # ── Phase 2: Send ALL results back at once to the LLM ─────────────
    final_response = client.responses.create(
        model=MODEL,
        previous_response_id=response.id,
        input=tool_outputs
    )
    return final_response


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------


def main():
    print_header()
    while True:
        question = input("\nYou > ")
        if question.lower() in ("exit", "quit", "cls"):
            break

        response = client.responses.create(
            model=MODEL,
            input=[
                {"role":"system", "content":SYSTEM_PROMPT},
                {"role": "user", "content":question}
            ],
            tools=TOOLS
        )
        console.print(f"[yellow bold]First Response :>[/yellow bold]\n\n")
        pprint(response.model_dump())
        # for item in response.output:
        #     print("\n\n",item)
        
        # Execute requested tools.
        final_response = handle_tool_calls(response)
        usage = final_response.usage
        console.print()
        console.print(
            f"[bold cyan]AI > {final_response.output_text}[/bold cyan]\n"
        )

        console.print(
            # Panel(
                Align.center("[bold yellow]Token Usage"
                    f"[bold yellow]Input Tokens > {usage.input_tokens} "
                    f"|| Output Tokens > {usage.output_tokens} "
                    f"|| Total Tokens > {usage.total_tokens}[/bold yellow]"
                    ), style="yellow"
            # )
        )

if __name__ == "__main__":

    main()