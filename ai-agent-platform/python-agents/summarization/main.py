import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from base.agent import BaseAgent
import asyncio

class SummaryAgent(BaseAgent):
    async def process(self, task_id, context):
        prompt = f"Summarize this data into key bullet points: {context}"
        return await self.generate(prompt) # <--- ADDED await

if __name__ == "__main__":
    agent = SummaryAgent("Summary", "agent.data.done", "agent.summary.done")
    asyncio.run(agent.run())