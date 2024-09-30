import chainlit as cl
from learnsherpa_ai.crew import AgentBooksV1Crew
from learnsherpa_ai.main import run_crew
import asyncio

@cl.on_chat_start
async def start():
    cl.user_session.set("crew_instance", AgentBooksV1Crew())
   
    welcome_message = """
    Welcome to the Book Recommendation System!
    To get started, please enter the genre of books you're interested in.
    For example, you could type:
    - Science Fiction
    - Productivity
    - Finance
    - Fantasy
    - History
    Once you enter a genre, I'll generate a report of the best books in that category.
    """
   
    await cl.Message(content=welcome_message).send()

@cl.on_message
async def main(message: cl.Message):
    crew_instance = cl.user_session.get("crew_instance")
   
    genre = message.content.strip()
    # Inform the user that the report generation has started
    await cl.Message(content=f"Generating report for genre: {genre}. This may take a few minutes...").send()
   
    try:
        # Create a task for running the crew
        crew_task = asyncio.create_task(cl.make_async(run_crew)(crew_instance, genre))
        
        # Create tasks for sending update messages
        update_messages = [
            ("The best_books_researcher agent is finding the best books...", 30),
            ("The agent_goodreads expert is searching for info on Goodreads...", 60),
            ("The reddit_reviewer is analyzing discussions on Reddit...", 90),
            ("The orchestrator is compiling the final report...", 120)
        ]
        
        update_tasks = [send_update_message(msg, delay) for msg, delay in update_messages]
        
        # Wait for all tasks to complete
        await asyncio.gather(crew_task, *update_tasks)
        
        report_path = f"reports/{genre.replace(' ', '_').lower()}_report_latest.txt"
       
        with open(report_path, 'r') as f:
            report_content = f.read()
       
        await cl.Message(content=f"Report generated for genre: {genre}").send()
        await cl.Message(content=report_content).send()
   
    except Exception as e:
        error_message = f"An error occurred while generating the report: {str(e)}"
        await cl.Message(content=error_message).send()
   
    # Prompt the user for the next genre
    await cl.Message(content="Would you like to get recommendations for another genre? If so, please enter the genre.").send()

async def send_update_message(message, delay):
    await asyncio.sleep(delay)
    await cl.Message(content=message).send()