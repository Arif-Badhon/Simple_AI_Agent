from agent import SimpleAgent

# Create an agent
agent = SimpleAgent()

# Test the agent
queries = [
    "What is the capital of France?",
    "Calculate 25 * 4 + 10"
]

for query in queries:
    print(f"Query: {query}")
    response = agent.run(query)
    print(f"Response: {response}")
    print("-" * 50)