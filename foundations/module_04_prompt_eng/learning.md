# Module 04 – Prompt Engineering Fundamentals

> **Module:** 04  
> **Topic:** Prompt Engineering Fundamentals  
> **Objective:** Learn how prompt design influences the quality, consistency, and structure of LLM responses.

---

# Learning Objectives

After completing this module, you should be able to:

- Define Prompt Engineering.
- Explain why prompt quality matters.
- Describe the anatomy of a good prompt.
- Understand Zero-shot, One-shot, and Few-shot prompting.
- Use Role prompting and Constraint prompting.
- Compare different prompting techniques.
- Understand when Prompt Engineering is useful in modern AI systems.

---

# What is a Prompt?

A prompt is the input we provide to a Large Language Model (LLM).

Examples:

Question:

```text
Explain recursion.
```

Instruction:

```text
Summarize the following article.
```

Conversation:

```text
How do I deploy a FastAPI application?
```

Everything we send to the model is a prompt.

---

# What is Prompt Engineering?

Prompt Engineering is the process of designing prompts that help an LLM produce better, more reliable, and more consistent responses.

Good prompt engineering is not about "magic phrases." It is about communicating requirements clearly and reducing ambiguity.

---

# Why Prompt Engineering Matters

Imagine asking a software engineer:

> Build a website.

This request is ambiguous.

Now imagine saying:

> Build a responsive portfolio website using HTML, CSS, and JavaScript. Include a navigation bar, project gallery, contact form, and dark mode.

The second request is much more likely to produce the desired result.

LLMs behave similarly. The more precise and complete the prompt, the more likely the output will match your expectations.

---

# Anatomy of a Good Prompt

A well-designed prompt often contains:

- Task
- Context
- Constraints
- Desired Output Format
- Examples (optional)

Example:

Task:

```text
Explain recursion.
```

Context:

```text
The audience is a first-year computer science student.
```

Constraints:

```text
Maximum 150 words.
```

Output Format:

```text
Use bullet points.
```

---

# Prompting Techniques

## 1. Basic Prompt

Only the task is provided.

Example:

```text
Explain recursion.
```

The model decides everything else.

---

## 2. Role Prompt

Assign a role or persona to the model.

Example:

```text
You are a university professor.

Explain recursion.
```

The role influences tone, depth, and style.

---

## 3. Constraint Prompt

Provide explicit rules.

Example:

```text
Explain recursion.

Rules:

- Maximum 100 words
- Use simple English
- Give one analogy
- Do not include code
```

Constraints reduce ambiguity and improve consistency.

---

## 4. Zero-shot Prompting

The model receives only the task.

Example:

```text
Translate this sentence into French.

Hello.
```

No examples are provided.

---

## 5. One-shot Prompting

Provide a single example before the actual task.

Example:

```text
Question:
What is a variable?

Answer:
A variable stores information.

Question:
Explain recursion.
```

The example demonstrates the expected style or format.

---

## 6. Few-shot Prompting

Provide multiple examples.

Example:

```text
Question:
What is a variable?

Answer:
...

Question:
What is a function?

Answer:
...

Question:
Explain recursion.
```

The model learns the expected pattern from several examples.

---

# Prompt Engineering in Modern AI

Prompt Engineering is still important, but it is no longer the primary skill in AI Engineering.

Modern AI systems rely on:

- Retrieval-Augmented Generation (RAG)
- Tool Calling
- Function Calling
- Agents
- Memory
- Planning
- Evaluation

Prompt Engineering is one component within these larger systems.

---

# Module Implementation

This module introduced two files:

## prompt_builder.py

Contains reusable prompt templates.

Examples:

- Basic Prompt
- Role Prompt
- Constraint Prompt
- Zero-shot
- One-shot
- Few-shot

Separating prompt templates from application logic improves maintainability and mirrors real-world AI projects.

---

## main.py

The application:

1. Accepts a user question.
2. Generates six different prompt variations.
3. Sends each prompt to the LLM.
4. Displays each response.
5. Tracks token usage.
6. Compares the results.

The same question is reused so that only the prompting strategy changes, making it easier to observe the effect of each technique.

---

# Key Takeaways

- Prompt Engineering reduces ambiguity.
- Better prompts generally produce more useful outputs.
- Examples help guide the model toward the desired format.
- Constraints improve consistency.
- Prompt Engineering complements, rather than replaces, good system design.

---

# Interview Questions

### What is Prompt Engineering?

Prompt Engineering is the practice of designing prompts that guide an LLM toward accurate, consistent, and useful responses.

---

### What is the difference between Zero-shot and Few-shot prompting?

Zero-shot provides only the task.

Few-shot provides multiple examples before the task to establish the desired pattern.

---

### When should Few-shot prompting be used?

When consistent formatting, reasoning style, or output structure is important and a few examples can clarify expectations.

---

### Is Prompt Engineering enough to build production AI systems?

No.

Production systems also require architecture for retrieval, tool integration, memory, evaluation, monitoring, security, and scalability.

---

# Things to Remember

- A prompt is any input sent to an LLM.
- Prompt Engineering is about clarity, not clever wording.
- Task + Context + Constraints + Format + Examples is a useful mental checklist.
- Role prompting changes *how* the model responds.
- Few-shot prompting teaches the model through examples.
- Prompt Engineering is one part of a larger AI engineering toolkit.

---

# Next Module Preview

**Module 05 – Structured Outputs**

Instead of asking the model to generate free-form text, we will instruct it to produce structured, machine-readable outputs (such as JSON) that applications can validate and process automatically.

This marks the transition from conversational AI to AI-powered software systems.