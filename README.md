# AI Research Agent

An autonomous AI agent that researches any topic by searching the web and writing a structured report.

Live Demo: https://huggingface.co/spaces/olsionh/research-agent

## How It Works

1. User enters a research topic
2. The agent autonomously decides what to search
3. It searches multiple times, analyzing each result
4. It synthesizes everything into a structured report with sources
5. User can download the report

## Features

- Autonomous multi-step web search using Tavily
- Live agent activity — watch the agent think and search in real time
- Search history saved per session
- Download report as .txt
- Built with LangGraph ReAct agent pattern

## Tech Stack

- Framework: LangGraph
- LLM: OpenAI GPT-4o-mini
- Search: Tavily Search API
- UI: Streamlit
- Containerization: Docker
- Deployment: Hugging Face Spaces

## What Makes This Different From RAG

RAG retrieves from a fixed document. This agent autonomously decides what to search, when to search again, and how to synthesize information from live web results. It reasons across multiple steps before producing an answer.

## Run Locally

    git clone https://github.com/olsionh/research-agent.git
    cd research-agent
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    streamlit run app.py

## Limitations

- Requires OpenAI and Tavily API keys
- Report quality depends on Tavily search results
- No persistent storage between sessions

## Future Improvements

- Add PDF export
- Support follow-up questions on the same topic
- Add source credibility scoring
- Multi-agent version where one agent critiques the other
