
# Imports for agent classes, memory management, and utilities that together enable the stepwise, modular orchestration of the question-answering process.
from app.agents.answerer import AnswerAgent         # Generates answers using input question and any external context retrieved.
from app.agents.escalation import EscalationHandler
from app.agents.evaluator import EvaluatorAgent     # Assesses generated answers for factual grounding and confidence score.
from app.agents.planner import PlannerAgent         # Decides whether external context is necessary, and if so, how many items to retrieve.
from app.agents.retriever import RetreiverAgent     # Responsible for retrieving external context or information as directed by the planner.
from app.memory.long_term_memory import LongTermMemory  # Handles persistence of completed Q&A events for future reference.
from app.memory.session_memory import SessionMemory      # Maintains conversational memory (turns) for each session.
from app.utils.metrics import Metrics               # Tracks and logs operational events and internal agent metrics.

# A confidence score threshold (between 0 and 1) that an answer's evaluation must meet or exceed to be deemed successful.
CONFIDENCE_THRESHOLD = 0.6
# Upper limit on the number of attempts (cycles through the reasoning pipeline) before escalation or fallback is triggered.
MAX_RETRIES  = 2

class AgentController:
    """
    Manages the full end-to-end process of replying to user queries, coordinating all agent modules.
    This includes: planning pipeline steps; optionally retrieving context; generating an answer;
    evaluating its quality; and recording interactions to memory. If required, the process can retry or escalate.
    """

    def __init__(self):
        # Instantiate each agent, memory handler, and metrics logger to be used throughout the workflow.
        self.planner = PlannerAgent()
        self.retriever = RetreiverAgent()
        self.answerer = AnswerAgent()
        self.evaluator = EvaluatorAgent()
        self.session_memory = SessionMemory()
        self.long_term_memory = LongTermMemory()
        self.metrics = Metrics()
        self.escalation = EscalationHandler()

    def run(self, query: str, session_id: str):
        """
        Orchestrate one complete question answering cycle:
        1. Record the user query in session memory.
        2. Use the planner to determine if retrieval is warranted.
        3. If retrieval is needed, collect external context; else, use only the conversation so far.
        4. Generate a candidate answer using the answerer.
        5. Evaluate that answer for factual grounding and confidence.
        6. If the evaluation is satisfactory and confident, update memory and return the result.
        7. On failure, retry up to MAX_RETRIES; if confidence remains insufficient, escalate and record.
        Returns a status dictionary indicating either a successful answer or a need for escalation.
        """

        retries = 0

        # Step 1: Add the user query to the session's history.
        self.session_memory.add(session_id, "user", query)

        while retries < MAX_RETRIES:
            # Step 2: Decide plan of action.
            plan = self.planner.plan(query)
            self.metrics.log("plan_created", plan)

            # Step 3: Optionally retrieve context as needed by the plan.
            if plan['needs_retrieval'] == "yes":
                context = self.retriever.retrieve(
                    query,
                    int(plan['top_k'])  # The quantity of context pieces the planner suggests.
                )
                self.metrics.log("retrival_completed", {"chunks": len(context)})
            else:
                context = []

            # Step 4: Produce an answer using the current query and context.
            answer = self.answerer.answer(query, context)
            self.metrics.log("answer_generated", {"answer": answer})

            # Step 5: Analyze answer quality and confidence.
            eval = self.evaluator.evaluate(
                query=query, 
                context=context, 
                answer=answer
            )
            self.metrics.log("evaluation_completed", eval)

            # Step 6: If answer meets criteria, update memory and return a success response.
            if eval['grounded'] and eval['confidence'] >= CONFIDENCE_THRESHOLD:
                self.session_memory.add(session_id, "assistant", answer)
                self.long_term_memory.record({
                    "query": query,
                    "answer": answer,
                    "evaluation": eval,
                    "retries": retries
                })
                return {
                    "status": 'success',
                    "answer": answer,
                    "evaluation": eval
                }

            # Otherwise, prepare to try again.
            retries += 1
        
        # Step 7: Exhausted retries—escalate to a human or fallback handler and record.
        escalation = self.escalation.escalate(
            "Low Confidence after retries",
            {"query": query}
        )

        self.long_term_memory.record({
            "query": query,
            "status": "escalated"
        })
        return escalation

