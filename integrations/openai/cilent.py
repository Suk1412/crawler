import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ["OPENAI_BASE_URL"],
)

response = client.responses.create(
    model=os.environ["OPENAI_MODEL"],
    input="用一句话解释:CSS selector 是什么？",
)

print(response.output_text)
