import chainlit as cl
from learnsherpa_ai.main import run as generate_report
from rag_reports.chat_interface import BookChatInterface
from rag_reports.populate_db import populate_database
from learnsherpa_ai.crew import AgentBooksV1Crew
from learnsherpa_ai.main import run_crew
import asyncio
import os

# Global variables
chat_interface = None
genre = None
report_file = None

@cl.on_chat_start
async def start():
    global crew_instance
    # Initialize crew instance
    crew_instance = cl.user_session.get("crew_instance", None)
    if not crew_instance:
        crew_instance = AgentBooksV1Crew()
        cl.user_session.set("crew_instance", crew_instance)

    # Welcome message
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
    global genre, crew_instance, chat_interface
    
    if not chat_interface:  # Report generation part
        genre = message.content.strip()
        await cl.Message(content=f"Generating report for genre: {genre}. This may take a few minutes"
                         "... Why not give your grandma a call while our agents work on it?" ).send()
        

        try:
            crew_task = asyncio.create_task(cl.make_async(run_crew)(crew_instance, genre))

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

            # Send the report to the user
            await cl.Message(content=f"Report generated for genre: {genre}").send()
            await cl.Message(content=report_content).send()

            await cl.Message(content="Populating the database with the generated report...").send()

            # Initialize the chat interface after the report and database are ready
            populate_database()
            chat_interface = BookChatInterface("Learn_sherpa_ai")  

            await cl.Message(content=f"Report generated and database populated for {genre}. You can now ask questions about the books!").send()

        except Exception as e:
            # Handle any errors that occurred during the report generation
            error_message = f"An error occurred while generating the report: {str(e)}"
            await cl.Message(content=error_message).send()

    else:  # Chat interaction part
        thinking_msg = cl.Message(content="Thinking...")
        await thinking_msg.send()

        try:
            response = chat_interface.get_response(message.content)
            await process_response(response)
        except Exception as e:
            await cl.Message(content=f"An error occurred: {str(e)}").send()
        finally:
            await thinking_msg.remove()


async def process_response(response):
    # Send the main answer
    await cl.Message(content=response['answer']).send()
    
    # Process sources if available
    if response['sources']:
        sources = response['sources'].split('\n')
        elements = [cl.Text(name="Source", content=source, display="inline") for source in sources]
        
        if elements:
            await cl.Message(
                content="Sources:",
                elements=elements
            ).send()
    else:
        await cl.Message(content="No specific sources found for this information.").send()


async def send_update_message(message, delay):
    await asyncio.sleep(delay)
    await cl.Message(content=message).send()

if __name__ == "__main__":
    cl.run()
