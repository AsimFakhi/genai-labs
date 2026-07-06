# uv run python -m foundations.module_06_tool_calling.main
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
import json
import re

from shared.settings import get_settings
from foundations.module_06_tool_calling.prompts import SYSTEM_PROMPT
from foundations.module_06_tool_calling.tools import TOOLS, TOOLS_MAP, execute_read_only_sql


settings = get_settings()
console = Console()

client = OpenAI(api_key=settings.openai_api_key)
MODEL = settings.gpt_nano


def print_header():
    terminal_width = console.size.width
    console.print(
        Panel(
            Align.center(
                "[bold cyan] Module 06 - Tool Calling[/bold cyan]\n"
                f"Model : {MODEL}"
            ),
            width=terminal_width - 4
        )
    )


def extract_sql_from_text(text: str) -> str | None:
    """
    Extract a SQL SELECT query from model output text.
    Returns the SQL string or None if no SQL found.
    """
    code_block_pattern = r'```sql\s*(.*?)\s*```'
    match = re.search(code_block_pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    select_pattern = r'(SELECT\s+.+?)(?:;|$)'
    match = re.search(select_pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    return None


def handle_tool_calls(response, user_question):
    """
    Execute every tool requested by the model.
    If model returns SQL as text instead of calling the tool,
    manually execute it and feed result back via a fresh conversation.
    """
    current_response = response
    round_num = 0
    executed_calls = set()
    
    while True:
        round_num += 1
        console.print(f"\n[dim]--- Tool Round {round_num} ---[/dim]")
        
        for item in current_response.output:
            console.print(f"[dim]Model output type: {item.type}[/dim]")
            if item.type == "function_call":
                console.print(f"[dim]  → wants: {item.name}({item.arguments})[/dim]")
            elif item.type == "message":
                text = item.content[0].text[:150] if item.content else "empty"
                console.print(f"[dim]  → text: {text}...[/dim]")
        
        function_calls = [
            item for item in current_response.output
            if item.type == "function_call"
        ]
        
        # CASE 1: Model used tools properly → execute them
        if function_calls:
            tool_outputs = []
            for call in function_calls:
                call_key = (call.name, call.arguments)
                
                if call_key in executed_calls:
                    console.print(f"[yellow]Skipping duplicate: {call.name}[/yellow]")
                    tool_outputs.append({
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": "Already executed. Use previous result."
                    })
                    continue
                
                executed_calls.add(call_key)
                console.print(f"\n[yellow]Calling Tool[/yellow] : {call.name}")
                
                tool = TOOLS_MAP.get(call.name)
                if tool is None:
                    tool_outputs.append({
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": f"Error: Unknown tool '{call.name}'"
                    })
                    continue

                arguments = json.loads(call.arguments)
                result = tool(**arguments)
                
                display = result[:300] + "..." if len(result) > 300 else result
                console.print(f"[dim]Result: {display}[/dim]")
                
                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": call.call_id,
                    "output": result
                })

            console.print(f"\n[dim]Sending {len(tool_outputs)} result(s) back...[/dim]")
            current_response = client.responses.create(
                model=MODEL,
                previous_response_id=current_response.id,
                input=tool_outputs
            )
            continue
        
        # CASE 2: No function calls — check for SQL leakage
        output_text = current_response.output_text or ""
        leaked_sql = extract_sql_from_text(output_text)
        
        if leaked_sql:
            console.print(f"\n[red]⚠️ Model leaked SQL as text![/red]")
            console.print(f"[yellow]SQL: {leaked_sql[:80]}...[/yellow]")
            
            # Execute SQL ourselves
            console.print(f"[green]Executing SQL manually...[/green]")
            sql_result = execute_read_only_sql(leaked_sql)
            
            # ❌ CANNOT fake a function_call_output — API rejects fake call_id
            # ✅ INSTEAD: Start a fresh conversation with result baked in
            console.print(f"[dim]Restarting conversation with SQL result...[/dim]")
            
            current_response = client.responses.create(
                model=MODEL,
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_question},
                    {"role": "assistant", "content": f"I checked the database. Here's what I found:\n\nQuery: {leaked_sql}\n\nResults:\n{sql_result}\n\nBased on these results, answer the user's question concisely."}
                ]
            )
            continue  # Loop once more — model should now answer with text
        
        # CASE 3: No tools, no SQL — done
        console.print("[dim]No more tool calls or SQL. Breaking.[/dim]")
        break
    
    return current_response


def main():
    print_header()
    while True:
        question = input("\nYou > ")
        if question.lower() in ("exit", "quit", "cls"):
            break

        response = client.responses.create(
            model=MODEL,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}
            ],
            tools=TOOLS
        )

        final_response = handle_tool_calls(response, question)
        usage = final_response.usage
        
        console.print()
        console.print(f"[bold cyan]AI > {final_response.output_text}[/bold cyan]\n")
        console.print(
            Align.center(
                f"[bold yellow]Input Tokens > {usage.input_tokens} || "
                f"Output Tokens > {usage.output_tokens} || "
                f"Total Tokens > {usage.total_tokens}[/bold yellow]"
            ),
            style="yellow"
        )


if __name__ == "__main__":
    main()