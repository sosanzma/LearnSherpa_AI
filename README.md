# AI-Powered Book Recommendation System

## Overview

This project is an AI-powered book recommendation system that utilizes a crew of AI agents to search, analyze, and compile book recommendations based on user input. The system focuses on finding books in a specified genre, gathering recommendations from notable figures, and analyzing public opinion.

## Features

- Search for book recommendations in a specific genre by given people
- Identify top-rated books based on overall ratings and expert reviews
- Gather and summarize opinions from Reddit discussions
- Compile a comprehensive report with book recommendations, reviews, and summaries
- Generate an interactive infographic of recommended books

## Project Structure

- `main.py`: Entry point for running the crew locally
- `crew.py`: Defines the AI agents and their tasks
- `agents.yaml`: Configuration for AI agents
- `tasks.yaml`: Definition of tasks for the AI agents
- `tools/`: Contains custom tools used by the agents
  - `SearchTools.py`: Tool for searching book recommendations
  - `BookReviewTool.py`: Tool for finding top-rated books and reviews
  - `RedditOpinionSearch.py`: Tool for gathering opinions from Reddit

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your API keys:
     ```
     SERPER_API_KEY=your_serper_api_key
     OPENAI_API_KEY=your_openai_api_key
     ```

## Usage

### Running the Crew

To run the book recommendation system:

```python
from agent_books_v1.crew import AgentBooksV1Crew

inputs = {
    'genre': 'neuroscience',
    'person_1': 'Elon Musk',
    'person_2': 'Mark Zuckerberg',
    'person_3': 'Lex Fridman'
}

AgentBooksV1Crew().crew().kickoff(inputs=inputs)
```

### Training the Crew

To train the crew for a given number of iterations:

```
python main.py train 5 training_results.json
```

### Replaying Crew Execution

To replay the crew execution from a specific task:

```
python main.py replay task_id_here
```

### Testing the Crew

To test the crew execution and get results:

```
python main.py test 3 gpt-4
```

## Output

The system generates a comprehensive report saved as `book_recommendations_report.md`, which includes:

- List of recommended books
- Top-rated books in the specified genre
- Summaries of Reddit discussions for each book
- Brief descriptions and ratings

## Visualization

The project includes a React component (`book-infographic.tsx`) that creates an interactive infographic of the recommended books. This component can be integrated into a web application to display the results in a visually appealing manner.

## Customization

You can customize the AI agents and their tasks by modifying the `agents.yaml` and `tasks.yaml` files. Add new tools in the `tools/` directory and update the `crew.py` file to incorporate them into the agent's capabilities.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open-source and available under the [MIT License](LICENSE).
