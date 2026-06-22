import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from base.agent import BaseAgent
import asyncpg
import asyncio

class ReportAgent(BaseAgent):
    def __init__(self):
        super().__init__("Report", "agent.summary.done", "task.completed")
        self.db = None

    async def run(self):
        self.db = await asyncpg.connect("postgres://admin:password@localhost:5432/agents_db")
        await super().run()

    async def process(self, task_id, context):
        prompt = f"Generate a professional Markdown report based on this summary: {context}"
        report = await self.generate(prompt) # <--- ADDED await
        
        # Save the final report and mark task as COMPLETED
        if self.db:
            await self.db.execute(
                "INSERT INTO results (id, execution_id, data) VALUES ($1, $2, $3)",
                task_id, task_id, report
            )
            await self.db.execute(
                "UPDATE tasks SET status = 'COMPLETED' WHERE id = $1",
                task_id
            )
            print(f"[Report] Saved report and marked COMPLETED for task: {task_id}")
        
        return report

if __name__ == "__main__":
    agent = ReportAgent()
    asyncio.run(agent.run())