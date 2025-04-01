# ETHTaipei - ReAct Agent 

This project demonstrates the usage of LangGraph with a ReAct agent implementation, featuring various tools for helping with DeFi actions.

## Setup

1. Create and activate a virtual environment:
```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows

# OR using uv
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.\.venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

## Usage

Run the agent:
```bash
python main.py
```
m
## Project Structure

- `main.py`: Main entry point with the ReAct agent implementation
- `tools/`: Directory containing various tools used by the agent
- `requirements.txt`: Project dependencies
- `.env`: Environment variables (create from .env.example) 