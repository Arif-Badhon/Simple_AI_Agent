import gradio as gr
from agent import SimpleAgent

# Create an agent
agent = SimpleAgent()

def process_query(query):
    """Process the query using our agent"""
    response = agent.run(query)
    return response

# Create a Gradio interface
demo = gr.Interface(
    fn=process_query,
    inputs=gr.Textbox(lines=2, placeholder="Ask me anything..."),
    outputs=gr.Textbox(),
    title="Simple AI Agent",
    description="Ask a question or request a calculation"
)

# Launch the app
if __name__ == "__main__":
    demo.launch()