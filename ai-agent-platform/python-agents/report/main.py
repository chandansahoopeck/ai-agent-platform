from base.agent import BaseAgent
import asyncpg

class ReportAgent(BaseAgent):
    def __init__(self):
        super().__init__("Report", "agent.summary.done", "task.completed")
        self.db = None

    async def run(self):
        self.db = await asyncpg.connect("postgres://admin:password@localhost:5432/agents_db")
        await super().run()

    async def process(self, context):
        prompt = f"Generate a professional Markdown report based on this summary: {context}"
        response = self.generate(prompt)
        return response.text

if __name__ == "__main__":
    agent = ReportAgent()
    asyncio.run(agent.run())