import gradio as gr
import os
from agent_books_v1.crew import AgentBooksV1Crew

def generate_report(openai_api_key, serper_api_key, genre):
    # Set environment variables
    os.environ['OPENAI_API_KEY'] = openai_api_key
    os.environ['SERPER_API_KEY'] = serper_api_key

    # Create crew instance and generate report
    crew_instance = AgentBooksV1Crew()
    result = crew_instance.crew().kickoff(inputs={'genre': genre})
    
    # Generate a filename for the report
    filename = f"{genre.replace(' ', '_').lower()}_report.txt"
    
    # Write the result to a text file
    with open(filename, 'w') as f:
        f.write(str(result))
    
    return filename

# Create Gradio interface
iface = gr.Interface(
    fn=generate_report,
    inputs=[
        gr.Textbox(label="OpenAI API Key"),
        gr.Textbox(label="Serper API Key"),
        gr.Textbox(label="Book Genre")
    ],
    outputs=gr.File(label="Generated Report"),
    title="Agent Books V1: Book Recommendation Report Generator",
    description="Enter your API keys and desired book genre to generate a recommendation report."
)

# Launch the interface
iface.launch()
