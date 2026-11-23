import re

FORBIDDEN_WORDS =[
    "delete", "drop", "update", "insert", "truncate",
    "alter", "create", "modify", "remove", "replace",
]

def validate_question(question: str) -> bool:
    if not question or not question.strip():
        raise ValueError("Please enter a question.")

    question = question.lower().strip()

    for word in FORBIDDEN_WORDS:
        if re.search(rf"\b{word}\b", question):
            raise ValueError("Data modification operations are not supported. Please ask a read-only question.")

    return True