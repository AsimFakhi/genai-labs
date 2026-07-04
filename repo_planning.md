# AI Engineering Learning Repository - Project Guide

> **Version:** 0.1
> **Status:** Active
> **Last Updated:** Module 02 Completed

---

# Table of Contents

1. Conversation Restart Briefing
2. Repository Vision
3. Learning Philosophy
4. Technology Stack
5. Repository Structure
6. Coding Standards
7. Shared Components
8. Current Progress
9. Planned Learning Modules
10. Future Projects
11. Engineering Decisions
12. Lessons Learned
13. Conversation Restart Checklist

---

# 1. Conversation Restart Briefing

This repository is a structured AI Engineering learning project.

The goal is **not simply to learn LangChain or LangGraph**, but to understand the underlying concepts before introducing frameworks.

The learning approach is intentionally incremental.

Every module introduces only one or two new concepts.

Framework abstractions are introduced only after understanding the lower-level implementation.

The repository should eventually become both:

* an AI engineering portfolio
* a personal reference handbook

Every module contains:

* working code
* detailed learning notes
* practical exercises (future)
* optional assets

The preferred teaching style is:

* explain concepts first
* explain architecture
* compare alternatives
* implement
* reflect

---

# 2. Repository Vision

Primary goals:

* Learn modern AI Engineering
* Understand OpenAI APIs
* Master Prompt Engineering
* Learn LangChain
* Learn LangGraph
* Build production-quality AI applications
* Understand RAG
* Learn AI Agents
* Build end-to-end AI systems

The emphasis is on understanding **why** each abstraction exists.

---

# 3. Learning Philosophy

Always follow this order:

1. Problem
2. Concept
3. Architecture
4. Alternatives
5. Implementation
6. Reflection
7. Exercises

Never introduce frameworks before understanding the underlying concept.

---

# 4. Technology Stack

## Language

Python 3.13+

---

## Package Manager

uv

Single shared project environment.

Avoid multiple virtual environments unless a project requires conflicting dependencies.

---

## LLM Provider

OpenAI

Current model:

gpt-5.5

---

## SDK

OpenAI Python SDK

Purpose:

Direct communication with OpenAI before introducing frameworks.

---

## Future Frameworks

* LangChain
* LangGraph

These will be introduced only after learning the underlying concepts.

---

## Console

Rich

Purpose:

Beautiful terminal output.

---

## Configuration

Environment Variables

Shared `.env`

Shared settings module

---

# 5. Repository Structure

```text
genai-labs/

shared/
    settings.py

foundations/
    module_01_llm_basics/
        main.py
        learning.md

    module_02_chat_conversation/
        main.py
        learning.md

intermediate/

advanced/

tests/

.env
pyproject.toml
uv.lock
```

Each module should remain as self-contained as possible.

Only genuinely reusable code belongs inside `shared/`.

---

# 6. Coding Standards

Keep code educational.

Prefer readability over cleverness.

Avoid unnecessary abstractions.

Use descriptive variable names.

Comment only when explaining intent rather than obvious syntax.

Every module should build naturally upon previous modules.

---

# 7. Shared Components

Current shared components:

## settings.py

Responsibilities:

* Load environment variables.
* Validate configuration.
* Expose application settings.

Future shared utilities may include:

* logging
* helpers
* reusable UI components
* common prompts

Avoid moving module-specific logic into `shared/`.

---

# 8. Current Progress

| Module                         | Status     | Notes                 |
| ------------------------------ | ---------- | --------------------- |
| Module 01 – LLM Basics         | ✅ Complete | First OpenAI API call |
| Module 02 – Chat Conversations | ✅ Complete | Conversation history  |

---

# 9. Planned Learning Modules

## Foundations

### Module 01

LLM Basics

Status:

Completed

---

### Module 02

Conversation History

Status:

Completed

---

### Module 03

System Prompts

Topics:

* role
* system instructions
* assistant behavior
* constraints
* personalities

---

### Module 04

Prompt Engineering

Topics:

* zero-shot
* one-shot
* few-shot
* delimiters
* context
* prompting strategies

---

### Module 05

Structured Outputs

Topics:

* JSON
* Pydantic
* validation
* response parsing

---

### Module 06

Function Calling

Topics:

* tools
* functions
* structured actions

---

### Module 07

Why LangChain?

Topics:

* pain points
* abstractions
* chat models
* prompt templates

---

### Module 08

LangChain Fundamentals

Topics:

* Chat Models
* Prompt Templates
* Output Parsers

---

### Module 09

Memory

Topics:

* conversation memory
* summarization
* token management

---

### Module 10

Retrieval-Augmented Generation (RAG)

Topics:

* embeddings
* vector databases
* retrieval

---

### Module 11

Agents

Topics:

* planning
* tools
* reasoning

---

### Module 12

LangGraph

Topics:

* graphs
* state
* nodes
* edges
* workflows

---

### Module 13+

Production AI Engineering

Topics:

* evaluation
* observability
* deployment
* testing
* monitoring

---

# 10. Future Projects

The repository will eventually contain larger end-to-end projects built using the concepts learned.

Potential projects include:

| Project                      | Status  |
| ---------------------------- | ------- |
| Chat Assistant               | Planned |
| RAG Chatbot                  | Planned |
| Document QA System           | Planned |
| AI Research Assistant        | Planned |
| AI Coding Assistant          | Planned |
| Multi-Agent Workflow         | Planned |
| Personal Knowledge Assistant | Planned |

---

# 11. Engineering Decisions

## Environment

One shared uv environment.

Reason:

Simpler maintenance.

Reduced duplicate dependencies.

Suitable for a learning repository.

---

## Configuration

One shared `.env`

Shared settings module.

---

## Module Design

Every module should be independent.

Avoid unnecessary dependencies between modules.

---

## Learning Notes

Every module contains:

learning.md

Purpose:

Document concepts rather than implementation details alone.

---

## Console UI

Rich should be used consistently throughout the repository.

---

## Framework Introduction

OpenAI SDK first.

LangChain later.

LangGraph later.

Never hide complexity before understanding it.

---

# 12. Lessons Learned

## Module 01

Learned:

* OpenAI SDK
* API Keys
* Environment Variables
* Response Objects
* Token Usage

---

## Module 02

Learned:

* LLMs are stateless.
* Conversation history is managed by the application.
* Message roles (`user`, `assistant`).
* Token usage grows with conversation length.
* Context windows are finite.

---

# 13. Conversation Restart Checklist

If this document is pasted into a new ChatGPT conversation:

The assistant should:

* Continue from the current module.
* Preserve repository conventions.
* Maintain the educational teaching style.
* Explain concepts before implementation.
* Avoid skipping foundational understanding.
* Keep modules incremental.
* Prefer OpenAI SDK before introducing LangChain abstractions.
* Update this document whenever architecture, conventions, or roadmap changes.

Current state:

* Repository initialized.
* Shared configuration implemented.
* Module 01 complete.
* Module 02 complete.
* Next planned module: **Module 03 – System Prompts**.

## Things to Remember

- LLMs are general-purpose; system prompts specialize them.
- System prompts define **how** the AI behaves.
- User prompts define **what** the AI should do.
- The system message is typically the first message in the conversation.
- Every API request includes the entire conversation history, including the system prompt.
- System prompts influence behavior but do not guarantee correctness or security.