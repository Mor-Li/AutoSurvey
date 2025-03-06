# test openai key
from openai import OpenAI

# set openai endpoint
# OpenAI.api_base = "http://152.69.226.145:3000/v1"
# OpenAI.api_base = "http://142.171.55.117:3000/v1/chat/completions"
# OpenAI.api_base = "http://124.223.89.121:3000/v1/chat/completions"
# OpenAI.api_base = "http://142.171.55.117:3000"

client = OpenAI(api_key='sk-I6AFhSv1Qodu8FBx15126145600f4220A7D4Cc69Ef4810F7',
                base_url='http://152.69.226.145:3000/v1')

completion = client.chat.completions.create(
    model="gpt-4o",
    # model="gpt-4o-2024-11-20",
    messages=[
        {"role": "developer", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Fuck u"
        }
    ]
)

print(completion.choices[0].message.content)