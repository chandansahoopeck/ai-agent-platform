import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from base.agent import BaseAgent
import asyncio

class ResearchAgent(BaseAgent):
    async def process(self, task_id, context):
        prompt = f"Research the following topic and provide raw facts: {context}"
        return await self.generate(prompt) # <--- ADDED await

if __name__ == "__main__":
    agent = ResearchAgent("Research", "task.created", "agent.research.done")
    asyncio.run(agent.run())