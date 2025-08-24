# Refactor & Extend: Simple Tool-Using Agent

**Goal:** Turn a brittle, partially working agent into production-quality code, then extend it with a new tool and real tests.

---

## Table of Contents

- [Overview](#overview)
- [Architecture Diagram](#architecture-diagram)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Extending the Agent](#extending-the-agent)
- [Error Handling & Logging](#error-handling--logging)
- [Test Coverage](#test-coverage)
- [Design Principles](#design-principles)
- [Assignment Checklist](#assignment-checklist)

---

## Overview

This project implements a modular, extensible agent that can:
- Parse natural language queries
- Plan and execute tool calls (calculator, weather, knowledge base, currency conversion, etc.)
- Combine results and handle multi-step reasoning
- Validate and type-check all tool arguments and results
- Handle malformed or unexpected LLM outputs gracefully

---

## Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                   User Query                                      |
+-----------------------------------------------------------------------------------+
        |                                   |
        v                                   v
+---------------------+       +-----------------------------------+         +---------------------+
|    main.py (CLI)    +-----> |      agent/agent.py (Agent)       + <-----> |   agent/llm.py      |
+---------------------+       +-----------------------------------+         +---------------------+
                                            |                                         |
                                            v                                         v
+---------------------+       +-----------------------------------+       +---------------------+
|   Tool Registry     |<----->|       Tool Plan (PlanStepModel)   |<----->|   Tool Parsers      |
| constants/tool_*.py |       +-----------------------------------+       +---------------------+
+---------------------+               |                                       |
                                      v                                       v
+---------------------+       +---------------------+       +---------------------+
| Tool Handlers       |<----->| Tool Schemas        |<----->| Tool Types          |
| agent/handlers/     |       | agent/types/        |       | agent/types/        |
+---------------------+       +---------------------+       +---------------------+
        |                               |                           |
        v                               v                           v
+---------------------+       +---------------------+       +---------------------+
| Data Sources        |       | Logging/Monitoring  |       | Validation/Errors   |
| data/kb.json, etc.  |       | utils/logger.py     |       | pydantic, typeguard |
+---------------------+       +---------------------+       +---------------------+
        |                               |                           |
        v                               v                           v
+---------------------+       +---------------------+       +--------------------------+
| Test Suite          |       | Extensibility Layer |       | Latency Tracking         |
| tests/              |       | (add new tools)     |       | utils/latency_tracker.py |
+---------------------+       +---------------------+       +--------------------------+
```

---

## Project Structure

```
se1-agent-debug-assignment/
│
├── agent/                      # Core agent logic
│   ├── __init__.py
│   ├── agent.py                # Main orchestrator (answer function)
│   ├── llm.py                  # LLM interface / plan parser
│   ├── handlers/               # Tool-specific handlers
│   │   ├── __init__.py
│   │   ├── calc_handler.py
│   │   ├── temp_handler.py
│   │   ├── weather_handler.py
│   │   ├── fx_handler.py
│   │   └── kb_handler.py
│   ├── tools/               	# llm specific tools
│   │   ├── __init__.py
│   │   ├── calc_tools.py
│   │   ├── temp_tools.py
│   │   ├── weather_tools.py
│   │   ├── fx_tools.py
│   │   └── kb_tools.py
│   ├── llm_parsers/        	# llm specific parsers
│   │   ├── __init__.py
│   │   ├── calc_parser.py
│   │   ├── temp_parser.py
│   │   ├── weather_parser.py
│   │   ├── fx_parser.py
│   │   └── kb_parser.py
│   ├── types/               	# plan and tool types
│   │   ├── __init__.py
│   │   ├── plan_types.py
│   │   └── tool_types.py
│
├── data/                       # Static data / knowledge base
│   └── kb.json
├── utils/                      # Job-specific utilities
│   ├── __init__.py
│   ├── latency_tracker.py
│   └── logger.py
│
├── logs/                       # Auto-created log directory
│   ├── info.log
│   └── error.log
│
├── tests/                      # Unit / smoke tests
│   ├── __init__.py
│   ├── test_smoke.py
│   ├── test_calc.py
│   ├── test_temp.py
│   ├── test_weather.py
│   ├── test_fx.py
│   └── test_kb.py
├── constants/                 	# Constants
│   ├── miscellaneous_constants.py
│   ├── regex_constants.py
│   └── tool_constants.py
│
├── config/                     # Configuration
│   └── settings.py             # e.g., KB file path
│
├── main.py                     # CLI entrypoint
├── requirements.txt            # Dependencies
├── .env                        # Main environment file
├── .env.example                # Sample environment file
├── Makefile            		# Makefile
└── README.md                   # Documentation
```

---

## Quick Start

### Python 3.10+ recommended

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage Examples

Handled examples given as tasks:

```bash
python main.py "What is 12.5% of 243?"
# → 30.375

python main.py "Summarize today's weather in Paris in 3 words"
# → Mild and cloudy.

python main.py "Who is Ada Lovelace?"
# → Ada Lovelace was a 19th-century mathematician regarded as an early computing pioneer...

python main.py "Add 10 to the average temperature in Paris and London right now."
# → 28.0°C              # Although the actual result is 27.5°C, the expected output given in the task is 28.0°C.

python main.py "Convert the average of 10 and 20 USD into EUR."
# → 13.65
```

More Examples:
```bash
python main.py "Add 10 and multiply by 2 and multiply by 4 and then divide by 2 to the average temperature in dhaka and London."
# → 136.0°C

python main.py "What is 31 plus 5?"
# → 36.0

 python main.py "Add 10 to the individual temperature in Paris and London right now."
# → {'London': '27.0°C', 'Paris': '28.0°C'}              # Added 10 to cities individually

python main.py "Weather in Paris and London?"
# → {'Paris': 'Mild and cloudy.', 'London': 'Cool and rainy.'}

```

---

## Testing

Run all tests:

```bash
pytest -q
# or, if you want to ensure the correct module path is used:
PYTHONPATH=. pytest
```

To run test on specific tool:

```bash
PYTHONPATH=. pytest tests/test_<TOOL_NAME>.py # For example: PYTHONPATH=. pytest tests/test_weather.py
```

Expected Output:

```bash
(.venv) nahian@pop-os:~/optimizely_assignment/se1-agent-debug-assignment/se1-agent-debug-assignment$ PYTHONPATH=. pytest
============================================= test session starts =============================================
platform linux -- Python 3.10.12, pytest-8.4.1, pluggy-1.6.0
rootdir: /home/nahian/optimizely_assignment/se1-agent-debug-assignment/se1-agent-debug-assignment
plugins: typeguard-4.4.4
collected 36 items                                                                                            

tests/test_calc.py ..........                                                                           [ 27%]
tests/test_fx.py ......                                                                                 [ 44%]
tests/test_kb.py .....                                                                                  [ 58%]
tests/test_smoke.py ....                                                                                [ 69%]
tests/test_temp.py ......                                                                               [ 86%]
tests/test_weather.py .....                                                                             [100%]

============================================= 36 passed in 0.33s ==============================================
```

Tests include:
- Smoke tests for agent output
- Tool-specific tests (Calculator, Temperature, Weather, Knowledge-base and FX)
- Edge cases (invalid input, empty input, malformed LLM output)

---

## Extending the Agent

**To add a new tool:**

1. **Implement the Tool Handler:**  
   - Add your function in [`agent/handlers/`](agent/handlers/) naming it `<TOOL_NAME>_handler.py`.

2. **Define the Tool Schema:**  
   - Add a Pydantic model for your tool’s arguments in [`agent/types/tool_types.py`](agent/types/tool_types.py).
   - Add plan types in [`agent/types/plan_types.py`](agent/types/plan_types.py).

3. **Register the Tool:**  
   - Update [`constants/tool_constants.py`](constants/tool_constants.py) to add your tool to `TOOL_HANDLERS`, `TOOL_MODELS`, and `PARSERS`.

4. **Add a Parser:**  
   - Implement a parser function for your tool in [`agent/llm_parsers/`](agent/llm_parsers/) naming `<TOOL_NAME>_parser.py`.

5. **Add a Tool Logic:**  
   - Implement tool functions for your tool in [`agent/tools/`](agent/tools/) naming `<TOOL_NAME>_tools.py`.

6. **Write Tests:**  
   - Add tests for your tool in [`tests/`](tests/) naming `test_<TOOL_NAME>.py`.
   - You may also add relevant tests in [`tests/test_smoke.py`](tests/test_smoke.py).

7. **(Optional) Add Data:**  
   - If your tool needs data, add it to the [`data/`](data/) directory.

---

## Error Handling & Logging

- All tool execution is wrapped in robust error handling.
- Invalid or malformed tool plans are logged and do not crash the agent.
- All tool arguments are validated using Pydantic schemas.
- Latency and errors are tracked via [`utils/logger.py`](utils/logger.py) and [`utils/latency_tracker.py`](utils/latency_tracker.py).
- Rolling logger files will be zipped weekly to optimize storage, and the log files included in this repository are provided intentionally for reference.

---

## Test Coverage

The repository includes the following test files:

- [`test_smoke.py`](tests/test_smoke.py) – Verifies general agent behavior.  
- [`test_calc.py`](tests/test_calc.py) – Checks calculation functionalities.  
- [`test_temp.py`](tests/test_temp.py) – Tests temperature-related operations.  
- [`test_weather.py`](tests/test_weather.py) – Validates weather information retrieval.  
- [`test_fx.py`](tests/test_fx.py) – Ensures currency conversion works correctly.  
- [`test_kb.py`](tests/test_kb.py) – Confirms knowledge base responses.

All tests are located in the [`tests/`](tests/) directory and can be extended as new tools are added.

---

## Design Principles

- **Separation of Concerns:** Each layer (parsing, planning, execution, validation) is modular and independently testable.
- **Extensibility:** New tools can be added with minimal changes by updating handlers, tools, types, and parsers.
- **Robustness:** Handles malformed input, missing arguments, and tool errors gracefully.
- **Type Safety:** All tool arguments and results are validated using Pydantic models and typeguard.
- **Observability:** Logging and latency tracking are built-in for debugging and performance monitoring.
- **Testability:** Comprehensive test suite ensures correctness and reliability.

---

## Assignment Checklist

- ✅ Split responsibilities into modules/classes.
- ✅ Add schemas for tool plans; validate inputs and tool names.
- ✅ Make tool calls resilient and typed.
- ✅ Add one new tool (e.g., currency converter) and tests to prove extensibility.
- ✅ Update README with a detailed architecture diagram and clear instructions.
- ✅ Ensure code is robust against malformed LLM responses.

---


## Notes / Future Improvements

- While this code completes the assignment requirements, there is still room for improvement.  

- Some areas could be further refined or optimized, but due to the nature of this assignment as a test, certain clarifications could not be asked at the time.  

- A more complete or robust solution can be implemented once these confusions are resolved in the future.

- With proper guidance and clarification, the implementation could be significantly enhanced to achieve its full potential.

---

> Note: The fake LLM sometimes emits malformed JSON to simulate real-world flakiness. The agent is designed to handle such cases gracefully.

---