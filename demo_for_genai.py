from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyD9LdwEeX_gp-nPq17CdaXTh3gSVh9pxU47772525",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": "you should only reply related to coding context."},
        {"role": "user", "content": "give me a simple hindi poem!"}
    ]
)

print(response.choices[0].message.content)