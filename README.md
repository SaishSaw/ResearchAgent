# 🧠 ResearchAgent – Multi-Step AI Research Assistant

A dynamic AI research assistant built using LangChain Agents, Tavily Search, and Chainlit.
The system expands user queries, performs web research, aggregates results, and produces concise research summaries — all through an interactive UI.

# 🚀 Features

- 🔍 Automated Query Expansion
- 🌐 Web Search using Tavily
- 🧩 Agent-based Orchestration (LangChain + LangGraph)
- 🧠 LLM-powered Research Summarization
- 💬 Interactive UI using Chainlit
- ⚡ Async-safe execution for production

# Install dependencies
```
pip install -r requirements.txt
```

# Initialize the application
```
chainlit run main.py
```

# Project Structure
```
ResearchAgent/
│
├── main.py                # Chainlit app + agent orchestration
│
├── .env                   # API keys
├── pyproject.toml
└── README.md
```

# Tech Stack
Python3.12
Langchain
Chainlit
Tavily



