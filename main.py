import sys
from typing import NoReturn
from agent.agent import answer, AnswerResultType
from utils.latency_tracker import track_latency

@track_latency(__name__)
def main() -> NoReturn:
    """
    Entry point for the command-line interface.

    Reads a query from command-line arguments, passes it to the `answer` function,
    and prints the result.

    Usage:
        python main.py "your question here"

    Raises:
        SystemExit: If no query is provided in the command-line arguments.
        Any exception raised by `answer` will propagate.
    """
    
    if len(sys.argv) < 2:
        print("Usage: python main.py \"your question here\"")
        sys.exit(1)

    q: str = " ".join(sys.argv[1:])
    out: AnswerResultType = answer(q)
    print(out)

if __name__ == "__main__":
    main()
