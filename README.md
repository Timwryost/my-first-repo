# my-first-repo
This repository contains a simple demonstration of a concept called **promptware**. Promptware is a small tool that keeps track of tasks and uses AI to break each task down into actionable steps.

## Getting Started

The example script `promptware.py` stores tasks in `knowledge_base.json` and communicates with the OpenAI API to generate step-by-step instructions.

### Installation

1. Install the requirements:
   ```bash
   pip install openai
   ```
2. Set your OpenAI API key in the environment:
   ```bash
   export OPENAI_API_KEY=your_key_here
   ```

### Usage

Add a new task:
```bash
python promptware.py add "Build a personal website"
```

Process pending tasks and generate steps for each task:
```bash
python promptware.py process
```

View tasks and their status:
```bash
python promptware.py view
```

The script will ask OpenAI to break down tasks into small steps, print the steps, and wait for you to mark them as complete.
