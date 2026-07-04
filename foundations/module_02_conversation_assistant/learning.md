# Module 02 – Building a Conversation Assistant

## Goal

In Module 01, we learned how to send a single prompt to an LLM and receive a response.

In this module, we extended that application into a conversational assistant by maintaining the history of the conversation ourselves. This demonstrates one of the most important concepts in AI engineering: **LLMs are stateless**.

---

# Problem Statement

If we send only the latest question to the model, it has no knowledge of previous interactions.

Example:

```
User:
Explain recursion.

Assistant:
...

User:
Can you give another example?
```

If only the second question is sent to the API, the model has no idea what "another example" refers to.

The application must provide the missing context.

---

# Key Concept: LLMs Are Stateless

An LLM does not remember previous API calls.

Every request is independent.

The model only knows the information contained in the current request.

Therefore, maintaining conversation history is the responsibility of the application, not the model.

---

# Conversation History

We introduced a Python list to store every message exchanged during the session.

```python
conversation = []
```

Each message consists of:

* a **role**
* some **content**

Example:

```python
[
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi!"},
]
```

This list grows after every interaction.

---

# Message Roles

We learned about two message roles.

### User

Represents input from the human user.

```python
{
    "role": "user",
    "content": "Explain recursion"
}
```

### Assistant

Represents the model's previous responses.

```python
{
    "role": "assistant",
    "content": "Recursion is..."
}
```

In a later module, we will introduce the **system** role, which defines the assistant's behavior and instructions.

---

# Sending the Conversation

Instead of sending a single string:

```python
input=prompt
```

we now send the complete conversation:

```python
input=conversation
```

This allows the model to answer follow-up questions naturally because it receives the previous context.

---

# Updating the Conversation

After receiving a response:

```python
answer = response.output_text
```

we append it to the conversation.

```python
conversation.append(
    {
        "role": "assistant",
        "content": answer,
    }
)
```

The conversation history therefore grows after every exchange.

---

# Token Usage

The OpenAI response contains token statistics.

For each request we can inspect:

* Input Tokens
* Output Tokens
* Total Tokens

In this module, we improved the application by tracking the cumulative token usage across the entire conversation.

This provides visibility into how much the conversation costs and demonstrates that each successive request becomes larger because the entire conversation history is sent to the model.

---

# Program Flow

```
User enters prompt
        │
        ▼
Store user message
        │
        ▼
Conversation History
        │
        ▼
Send complete history to OpenAI
        │
        ▼
Receive assistant response
        │
        ▼
Store assistant response
        │
        ▼
Display answer and token usage
```

---

# Important Observation

As the conversation becomes longer:

* Input tokens increase.
* Response latency may increase.
* API cost increases.
* Eventually, the conversation may exceed the model's context window.

This leads to an important engineering challenge:

**How do we decide what information should be kept, summarized, retrieved, or discarded?**

This problem forms the foundation for memory management techniques used in LangChain, LangGraph, and Retrieval-Augmented Generation (RAG).

---

# Files Created

```
foundations/
└── module_02_chat_conversation/
    ├── main.py
    └── learning.md
```

---

# Key Concepts Learned

* Stateless LLMs
* Conversation History
* Message Roles (`user` and `assistant`)
* Context
* Context Window
* Token Usage
* Session-Level Metrics
* Follow-up Questions

---

# Key Takeaways

* LLMs do not remember previous requests.
* The application is responsible for maintaining context.
* Conversation history is simply a list of messages.
* Sending the full conversation enables natural dialogue.
* Longer conversations increase token usage and cost.
* Efficient context management is a core AI engineering challenge.

---

# Next Module

In the next module, we will introduce **System Prompts**.

A system prompt allows us to control the assistant's behavior, personality, expertise, response style, and constraints without changing the user's prompt.

This is the first step toward building specialized AI assistants.
