"""
Multi-Agent Controller Example

This example demonstrates how to use the multi-agent controller
for parallel processing and consensus-based answering.
"""

from app.orchestration.multi_agent_controller import MultiAgentController

def example_multi_agent_query():
    """
    Example of using the multi-agent controller.
    
    The multi-agent controller uses multiple worker agents to generate
    answers in parallel, then uses a critic and judge to determine
    the best final answer.
    """
    
    print("=== Multi-Agent Controller Example ===\n")
    
    # Initialize the controller
    controller = MultiAgentController()
    
    # Example query and context
    query = "What are the advantages of using RAG over fine-tuning?"
    context = [
        "RAG allows access to up-to-date information without retraining.",
        "Fine-tuning requires retraining the model for new information.",
        "RAG combines retrieval and generation for better accuracy."
    ]
    
    print(f"Query: {query}\n")
    print(f"Context: {context}\n")
    print("Processing with multi-agent system...\n")
    
    # Get multi-agent response
    result = controller.run(query, context)
    
    # Display results
    print("=" * 60)
    print("WORKER ANSWERS:")
    print("=" * 60)
    for i, answer in enumerate(result['answers'], 1):
        print(f"\nWorker {i}:")
        print(f"  {answer}")
    
    print("\n" + "=" * 60)
    print("CRITIQUE:")
    print("=" * 60)
    print(f"  {result['critique']}")
    
    print("\n" + "=" * 60)
    print("FINAL ANSWER (Judge Decision):")
    print("=" * 60)
    print(f"  {result['final_answer']}")
    print()

if __name__ == "__main__":
    example_multi_agent_query()

