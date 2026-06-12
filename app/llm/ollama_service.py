import httpx
import json
from app.core.logger import get_logger
from app.core.config import settings
from app.core.exceptions import LLMError
from typing import Generator


logger = get_logger("ollama")

OLLAMA_URL = settings.OLLAMA_URL


def generate_answer(prompt: str) -> str:
    logger.debug(f"Sending prompt to Ollama , length: {len(prompt)}")
       
    try:
        with httpx.Client(
            trust_env=False,
            timeout=settings.OLLAMA_TIMEOUT
        ) as client:

            response = client.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "stream": False,
                    "think": False
                    
                }
            )

            response.raise_for_status()
            answer = response.json()["message"]["content"]
            logger.debug(f"Ollama responded, answer length: {len(answer)}")
            return answer

    except Exception as e:
        logger.error(f"Ollama error: {str(e)}")
        raise LLMError(str(e))
    

def generate_answer_stream(prompt: str) -> Generator[str , None , None]:
    logger.debug(f"Sending streaming prompt to ollama, length: {len(prompt)}")

    try:
        with httpx.Client(trust_env= False , timeout = settings.OLLAMA_TIMEOUT) as client:
            with client.stream(
                "POST",
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "messages": [{"role": "user" , "content":prompt}],
                    "stream": True,
                    "think": False
                }
            ) as response:
                response.raise_for_status()
                
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        
                        token = chunk.get("message" , {}).get("content","")

                        if token:
                            yield token

                        if chunk.get("done", False):
                            logger.debug("Ollama stream completed")
                            break

    except Exception as e:
        logger.error(f"Ollama stream error: {str(e)}")
        raise LLMError(str(e))