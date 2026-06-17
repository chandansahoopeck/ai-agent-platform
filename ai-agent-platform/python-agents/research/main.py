import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from base.agent import BaseAgent
import asyncio

class ResearchAgent(BaseAgent):
    async def process(self, context):
        prompt = f"Research the following topic and provide raw facts: {context}"
        # Use the new helper method from BaseAgent
        return self.generate(prompt) 

if __name__ == "__main__":
    agent = ResearchAgent("Research", "task.created", "agent.research.done")
    asyncio.run(agent.run())