import re

FORBIDDEN_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER",
    "CREATE", "TRUNCATE", "REPLACE", "PRAGMA", "ATTACH", "DETACH",
]

def validate_sql(sql: str) -> str:
    if not sql or not sql.strip():
        raise ValueError("Generated SQL query is empty.")

    sql = sql.strip()

    if not re.match(r"^SELECT\b", sql, re.IGNORECASE):
        raise ValueError("Only SELECT queries are allowed.")

    upper_sql = sql.upper()
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", upper_sql):
            raise ValueError(f"Unsafe SQL detected: '{keyword}' statements are not allowed.")

    return sql