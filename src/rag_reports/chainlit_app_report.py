import chainlit as cl
from rag_reports.vector_db import VectorDB
from rag_reports.chat_interface import BookChatInterface
from typing import Dict

chat_interface = BookChatInterface("Learn_sherpa_ai")

@cl.on_chat_start
async def start():
    await cl.Message(content="Welcome to the Book Chat System! Ask me anything about the books in our database.").send()

@cl.on_message
async def main(message: cl.Message):
    thinking_msg = cl.Message(content="Thinking...")
    await thinking_msg.send()

    try:
        response = chat_interface.get_response(message.content)
        await process_response(response)
    except Exception as e:
        await cl.Message(content=f"An error occurred: {str(e)}").send()
    finally:
        await thinking_msg.remove()

async def process_response(response: Dict[str, str]):
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

if __name__ == "__main__":
    cl.run()