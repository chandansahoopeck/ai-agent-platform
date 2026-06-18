from base.agent import BaseAgent

class SummaryAgent(BaseAgent):
    async def process(self, context):
        prompt = f"Summarize this data into key bullet points: {context}"
        response = self.generate(prompt)
        return response.text

if __name__ == "__main__":
    agent = SummaryAgent("Summary", "agent.data.done", "agent.summary.done")
    asyncio.run(agent.run())