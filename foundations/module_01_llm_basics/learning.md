# Module 01 – LLM Basics

## Goal

The goal of this module was to make our very first successful API call to an LLM.

Rather than using LangChain or any other framework, we interacted directly with the OpenAI SDK so we could understand the fundamental building blocks first.

---

# What We Learned

## 1. OpenAI SDK

The OpenAI SDK is the official Python library provided by OpenAI.

It is responsible for:

- authenticating with the OpenAI API
- sending requests
- receiving responses
- handling errors
- exposing convenient Python objects

Instead of manually making HTTP requests, we use the SDK.

```python
from openai import OpenAI
```

---

## 2. API Key

Every request to OpenAI must be authenticated.

We store the API key inside a `.env` file instead of hardcoding it into our code.

Example:

```text
OPENAI_API_KEY=sk-...
```

This keeps secrets out of Git.

---

## 3. Settings

We created a shared `settings.py` file.

Its responsibility is to:

- load environment variables
- validate required values
- provide configuration to the rest of the application

This follows the idea of **centralized configuration**, meaning the application only has one place that knows where configuration comes from.

---

## 4. Creating the Client

We created an OpenAI client.

```python
client = OpenAI(api_key=settings.OPENAI_API_KEY)
```

Think of the client as a connection manager.

Instead of opening a new connection every time, the client knows how to communicate with OpenAI for all future requests.

---

## 5. Sending a Prompt

We asked the model a question.

```python
response = client.responses.create(
    model=settings.OPENAI_MODEL,
    input=prompt,
)
```

The important parts are:

- **model** → which LLM to use
- **input** → our prompt

The SDK sends this request over HTTPS to OpenAI's servers.

---

## 6. Reading the Response

The returned object contains much more than just text.

For this module we used

```python
response.output_text
```

which extracts the generated response as plain text.

---

## 7. Token Usage

The response also contains token statistics.

```python
usage = response.usage
```

We displayed

- Input Tokens
- Output Tokens
- Total Tokens

This helps us understand the cost of each request and is extremely useful when building production AI applications.

---

## 8. Rich Console

Instead of using Python's built-in `print()`, we used the Rich library.

Benefits:

- colored output
- better formatting
- cleaner user experience

Example:

```python
console.print("[bold cyan]AI > Hello[/bold cyan]")
```

---

# Flow of the Program

```
User Prompt
      │
      ▼
OpenAI Client
      │
      ▼
OpenAI API
      │
      ▼
LLM (GPT-5.5)
      │
      ▼
Response Object
      │
      ├── output_text
      └── usage
              ├── input_tokens
              ├── output_tokens
              └── total_tokens
```

---

# Files We Created

```
shared/
    settings.py

foundations/
    module_01_llm_basics/
        main.py

.env
```

---

# Key Concepts

- Environment Variables
- API Keys
- SDK
- Client
- Request
- Response
- Tokens
- Configuration Management

---

# Key Takeaways

- Every interaction with an LLM starts with an authenticated client.
- The OpenAI SDK handles communication with the API.
- The response contains much more than generated text.
- Token usage is important because it directly affects cost.
- Separating configuration from application logic makes projects easier to maintain and scale.

---

# Next Module

In the next module we will learn what actually happens inside a prompt and how different prompting styles influence the model's response.