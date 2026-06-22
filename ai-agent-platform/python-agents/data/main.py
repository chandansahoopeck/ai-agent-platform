import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from base.agent import BaseAgent
import asyncio

class DataAgent(BaseAgent):
    async def process(self, task_id, context):
        prompt = f"Extract structured JSON data from this research: {context}"
        return await self.generate(prompt) # <--- ADDED await

if __name__ == "__main__":
    agent = DataAgent("Data", "agent.research.done", "agent.data.done")
    asyncio.run(agent.run())