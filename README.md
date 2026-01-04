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


# Project Structure
ResearchAgent/
│
├── main.py                # Chainlit app + agent orchestration
├── agents/
│   ├── query_agent.py     # Query expansion agent
│   ├── search_agent.py    # Web search agent
│   └── conversational.py # Summarization agent
│
├── tools/
│   └── tavily_tool.py     # Tavily search tool
│
├── .env                   # API keys
├── pyproject.toml
└── README.md

