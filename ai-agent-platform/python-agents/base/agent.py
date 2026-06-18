import asyncio
import nats
from google import genai
import os

class BaseAgent:
    def __init__(self, name, subscribe_subject, publish_subject):
        self.name = name
        self.sub_subject = subscribe_subject
        self.pub_subject = publish_subject
        
        # Initialize the new Google GenAI client
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = "gemini-2.0-flash" # You can also use "gemini-2.0-flash"

    def generate(self, prompt):
        """Helper method to call the new Google GenAI SDK"""
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text

    async def run(self):
        nc = await nats.connect("nats://localhost:4222")
        print(f"[{self.name}] Connected to NATS. Listening on {self.sub_subject}")
        
        async def message_handler(msg):
            task_id = msg.data.decode()
            print(f"[{self.name}] Processing task: {task_id}")
            
            # 1. Fetch context from DB (Mocked for brevity)
            context = f"Data for task {task_id}" 
            
            # 2. Call LLM
            result = await self.process(context)
            
            # 3. Publish next event
            await nc.publish(self.pub_subject, f"{task_id}:{result}".encode())
            await msg.ack()

        await nc.subscribe(self.sub_subject, cb=message_handler)
        await asyncio.Future()  # Run forever

    async def process(self, context):
        raise NotImplementedError