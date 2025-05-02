import os
import json
from typing import Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))




class SimpleAgent:
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model_name = model_name
        self.tools = {
            "search": self.search_web,
            "calculate": self.calculate
        }

    def search_web(self, query: str) -> str:
        """Simple mock web search function"""
        # In a real application, you would integrate with a search API
        return f"Search results for: {query}"

    def calculate(self, expression: str) -> str:
        """Simple calculator function"""
        try:
            result = eval(expression)
            return f"The result of {expression} is {result}"
        except Exception as e:
            return f"Error calculating {expression}: {str(e)}"

    def think(self, query: str) -> Dict[str, Any]:
        """Process the query and decide on an action"""
        system_prompt = """
        You are an AI assistant that helps users by determining the appropriate action to take.
        You must choose one of the following tools:
        1. search - Use this when the user is asking for information
        2. calculate - Use this when the user wants to perform a calculation
        
        Output your decision as a valid JSON object with the following format:
        {"tool": "tool_name", "params": "parameters for the tool"}
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        response = client.chat.completions.create(model=self.model_name,
        messages=messages,
        temperature=0,
        max_tokens=150)

        try:
            decision_text = response.choices[0].message.content
            # Extract JSON from the response
            decision = json.loads(decision_text)
            return decision
        except Exception as e:
            # Fallback in case of parsing error
            return {
                "tool": "search",
                "params": query
            }

    def act(self, decision: Dict[str, Any]) -> str:
        """Execute the action based on the decision"""
        tool_name = decision.get("tool")
        params = decision.get("params")

        if tool_name in self.tools:
            tool = self.tools[tool_name]
            return tool(params)
        else:
            return "I don't know how to help with that."

    def run(self, query: str) -> str:
        """Main method to process a query"""
        decision = self.think(query)
        response = self.act(decision)
        return response