from app.agents.worker import WorkerAgent
from app.agents.critic import CriticAgent
from app.agents.judge import JudgeAgent

class MultiAgentController:
    def __init__(self):
        self.workers = [
            WorkerAgent("Expert A"),
            WorkerAgent("Expert B"),
            WorkerAgent("Expert C"),
        ]
        self.critic = CriticAgent()
        self.judge = JudgeAgent()

    def run(self, query: str, context: list[str]) -> dict:
        answers = [
            w.answer(query, context)
            for w in self.workers
        ]

        critique = self.critic.critique(query, answers, context)
        final_answer = self.judge.decide(answers, critique)

        return {
            "answers": answers,
            "critique": critique,
            "final_answer": final_answer
        }
