```python
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": (
        "You are DocuDigest, an assistant that summarizes "
        "legal contracts in plain English, highlights risks, "
        "and suggests mitigation steps."
    )},
    {"role": "user", "content": (
        "Please summarize the non-compete clause on page 5 "
        "and explain the key obligations."
    )},
  ]
)
print(response.choices[0].message.content)
	```
	