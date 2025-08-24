# Binary expressions (words or symbols)
BINARY_PATTERN = r"([\d\.]+[a-zA-Z]*)\s*(add|plus|sum|subtract|minus|multiply|times|divide|divided|[\+\-\*/])\s*([\d\.]+[a-zA-Z]*)"

# Percentage expressions
PERCENT_PATTERN = r"([\d\.]+[a-zA-Z]*)\s*%\s*of\s*([\d\.a-zA-Z]+)"

# Imperative expressions
IMPERATIVE_PATTERN = r"\b(add|plus|sum|subtract|minus|multiply|times|divide|divided)\b\s*(?:by\s*)?([\d\.]+[a-zA-Z]*)"

# Regex pattern to detect "average of X and Y"
AVERAGE_PATTERN = r"average of (\d+) and (\d+)"

# Regex pattern to clean expression strings before eval
CLEAN_EXPRESSION_PATTERN = r"[^\w\s\.\%\+\-\*\/]"