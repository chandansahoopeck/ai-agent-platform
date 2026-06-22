import asyncio
import nats
from google import genai
from google.genai import errors
import os

class BaseAgent:
    def __init__(self, name, subscribe_subject, publish_subject):
        self.name = name
        self.sub_subject = subscribe_subject
        self.pub_subject = publish_subject
        
        # Switch to 'latest' alias which often has separate/unexhausted quotas
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = "gemini-flash-latest" 

    async def generate(self, prompt):
        """Helper method with robust retries for rate limits"""
        max_retries = 3
        loop = asyncio.get_event_loop()
        
        def _call_api():
            return self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )

        for attempt in range(max_retries):
            try:
                response = await loop.run_in_executor(None, _call_api)
                return response.text
            except (errors.ClientError, errors.ServerError) as e:
                if "429" in str(e) or "503" in str(e):
                    # Wait a full 60 seconds to clear the 1-minute rolling window
                    wait_time = 60 
                    print(f"[{self.name}] Hit rate limit/high demand. Waiting {wait_time}s to clear the window... (Attempt {attempt+1}/{max_retries})")
                    await asyncio.sleep(wait_time)
                else:
                    raise e
            except Exception as e:
                print(f"[{self.name}] Unexpected error: {e}")
                raise e
                
        raise Exception(f"[{self.name}] Failed after {max_retries} retries.")

    async def run(self):
        nc = await nats.connect("nats://localhost:4222")
        print(f"[{self.name}] Connected to NATS. Listening on {self.sub_subject}")
        
        async def message_handler(msg):
            try:
                payload = msg.data.decode()
                if ':' in payload:
                    task_id, context = payload.split(':', 1)
                else:
                    task_id = payload
                    context = "No context provided."

                print(f"[{self.name}] Woke up for task: {task_id}")
                result = await self.process(task_id, context)
                print(f"[{self.name}] LLM Response received. Passing baton...")
                await nc.publish(self.pub_subject, f"{task_id}:{result}".encode())
                print(f"[{self.name}] Published to {self.pub_subject}")
                
            except Exception as e:
                print(f"[{self.name}] ERROR processing task: {e}")

        await nc.subscribe(self.sub_subject, cb=message_handler)
        await asyncio.Future()

    async def process(self, task_id, context):
        raise NotImplementedError