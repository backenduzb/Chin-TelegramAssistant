from cloudflare import Cloudflare
from config.settings import CLAUDE_LLMA_SECRET

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
                "content": "You are an AI assistant. You must answer ONLY in Uzbek language. Do not use English words. If the user writes in another language, still respond in Uzbek."
            },
            {
                "role": "user",
                "content": message
            }
        ],
    )
    return response.get('response')
    