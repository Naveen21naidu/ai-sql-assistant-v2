from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

schema_description = """
Tables:
Customers(customer_id, name, email, city)
Products(product_id, name, category, price)
Orders(order_id, customer_id, product_id, quantity, order_date)
"""

def generate_sql(question: str) -> str:
    prompt = f"""
    You are a SQL generator for a SQLite database with the following schema:
    {schema_description}

    Convert the question below into a single valid SQLite SELECT query.
    Respond with ONLY the raw SQL query. Do not include explanations,
    comments, or markdown formatting like ```sql.

    Question: {question}
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text.strip()