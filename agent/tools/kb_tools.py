import json
from typing import Any, Dict
from config.settings import KB_FILE_PATH
from ..types.tool_types import KBData
from utils.logger import get_logger
from typeguard import typechecked

logger = get_logger(__name__)

# Loading KB File once at module load
try:
    with open(KB_FILE_PATH, "r", encoding="utf-8") as f:
        KB_DATA: KBData = json.load(f)
        logger.info("Loaded KB data with %d entries", len(KB_DATA.get("entries", [])))
except Exception as e:
    logger.error("Failed to load KB data from %s: %s", KB_FILE_PATH, e)
    KB_DATA: KBData = {"entries": []}

@typechecked
def kb_lookup(q: str) -> str:
    """
    Lookup a query in the knowledge base (KB) JSON file.

    Args:
        q (str): The query string to search for in the KB.

    Returns:
        str: The summary of the KB entry if found. Returns "No entry found." if the query does not match any entry.

    Raises:
        Exception: For unexpected errors during KB lookup.
    """

    logger.info("Starting KB lookup for query: '%s'", q)
    try:
        for item in KB_DATA.get("entries", []):
            if q.lower() == item.get("name", "").lower():
                summary: str = item["summary"]
                logger.info("Found KB entry for '%s': %s", q, summary)
                return summary

        logger.info("No KB entry found for query: '%s'", q)
        return "No entry found."

    except Exception as e:
        logger.error("Error during KB lookup for query '%s': %s", q, e, exc_info=True)
        return f"KB error: {e}"
