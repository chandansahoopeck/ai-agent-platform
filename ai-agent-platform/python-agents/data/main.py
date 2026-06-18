from base.agent import BaseAgent
import json

class DataAgent(BaseAgent):
    async def process(self, context):
        prompt = f"Extract structured JSON data from this research: {context}"
        response = self.generate(prompt)
        return response.text # Returns JSON string

if __name__ == "__main__":
    agent = DataAgent("Data", "agent.research.done", "agent.data.done")
    asyncio.run(agent.run())