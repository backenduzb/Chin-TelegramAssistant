from cloudflare import Cloudflare
from config.settings import CLAUDE_LLMA_SECRET
from config.data import CONTENT

async def get_request_data(message: str):
        
    client = Cloudflare(
        api_token=CLAUDE_LLMA_SECRET, 
    )
    response = client.ai.run(
        model_name="@cf/meta/llama-3-8b-instruct",
        account_id="67a0e61f880887515569ec653131c90f",
        messages=[
            {
                "role": "system",
                "content": CONTENT
            },
            {
                "role": "user",
                "content": message
            }
        ],
    )
    return response.get('response')
    