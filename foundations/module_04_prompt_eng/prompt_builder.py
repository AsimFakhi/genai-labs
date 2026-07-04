"""
Prompt templates user for comparing deffirent prompting techniques.
"""

def basic_prompt(question:str)->str:
    return question

def role_prompt(question:str) -> str:
    return f"""
You are an expereienced computer science professor.
Answer the following question clearly and accurately.

Question:
{question}
""".strip()

def constraint_prompt(question:str)->str:
    return f"""
Answer the following question.

Rules:
- Maximum 100 words.
- Use simple English
- Give exactly one real-world analogy
- Do not include code.

Question:
{question}
""".strip()

def zero_shot_prompt(question: str) -> str:
    return f"""
Explain the following topic to someone with no technical background.

Question:
{question}
""".strip()


def one_shot_prompt(question: str) -> str:
    return f"""
Example

Question:
What is a variable?

Answer:
A variable is like a labeled box that stores information so you can use it later.

Now answer the next question.

Question:
{question}
""".strip()


def few_shot_prompt(question: str) -> str:
    return f"""
Examples

Question:
What is a variable?

Answer:
A variable stores information.

Question:
What is a loop?

Answer:
A loop repeats a task until a condition changes.

Question:
What is a function?

Answer:
A function is a reusable block of code.

Now answer this question.

Question:
{question}
""".strip()

PROMPTS = {
    "Basic Prompt": basic_prompt,
    "Role Prompt": role_prompt,
    "Constraint Prompt": constraint_prompt,
    "Zero Shot": zero_shot_prompt,
    "One Shot": one_shot_prompt,
    "Few Shot": few_shot_prompt
}