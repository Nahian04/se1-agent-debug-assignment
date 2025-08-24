# Binary expressions (words or symbols)
BINARY_PATTERN = r"([\d\.]+[a-zA-Z]*)\s*(add|plus|sum|subtract|minus|multiply|times|divide|divided|[\+\-\*/])\s*([\d\.]+[a-zA-Z]*)"

# Percentage expressions
PERCENT_PATTERN = r"([\d\.]+[a-zA-Z]*)\s*%\s*of\s*([\d\.a-zA-Z]+)"

# Imperative expressions
IMPERATIVE_PATTERN = r"\b(add|plus|sum|subtract|minus|multiply|times|divide|divided)\b\s*(?:by\s*)?([\d\.]+[a-zA-Z]*)"

# Regex to detect temperature queries
TEMPERATURE_PATTERN = r"(average|avg|total|sum|maximum|minimum|max|min)?\s*(?:of|the|for)?\s*temperature (?:in|at) (.+?)(?: right now|\?|$)"

# Regex to clean non-word characters from city part
CITY_CLEAN_PATTERN = r"[^\w\s]"

# Regex to split words/cities
CITY_SPLIT_PATTERN = r"[ ,?]+| and "

# Regex to detect weather queries
WEATHER_PATTERN = r"weather(?: in| of)? (.+?)(?: right now|\?|$)"

# Regex to extract numeric temperature from a string like "31.36°C" or "Temperature data unavailable. Default for Dhaka: 31°C"
NUMERIC_TEMPERATURE_PATTERN = r"[-+]?\d*\.?\d+"

# Regex pattern to detect "average of X and Y"
AVERAGE_PATTERN = r"average of (\d+) and (\d+)"

# Regex pattern to clean expression strings before eval
CLEAN_EXPRESSION_PATTERN = r"[^\w\s\.\%\+\-\*\/]"