import time
import argparse
import json
import os
from tqdm import tqdm
import logging 
from openai import OpenAI


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_API_RETRY = 5
os.environ["http_proxy"] = "http://localhost:7890"
os.environ["https_proxy"] = "http://localhost:7890"

def get_res(user_prompt: str,  api_key: str, max_tokens: int = 1024):
    logging.basicConfig(level=logging.INFO)
    for i in range(MAX_API_RETRY):
        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model='gpt-4',
                max_tokens=max_tokens,
                temperature=0.0,
                messages=[{
                    'role': 'user',
                    'content': user_prompt,
                }],
            )
            content = response.choices[0].message.content
            logger.info(content)
            return content
        except Exception as e:
            logger.error(e)
            time.sleep(20)
    logger.error(f'Failed after {MAX_API_RETRY} retries.')
    return 'error'