# Learnsherpa AI : Your chatbot AI-Powered Book Discovery Assistant

## 📚 Discover Your Next Great Read with Ease

Are you tired of endlessly scrolling through book recommendations, unsure which ones are truly worth your time? Enter Learnsherpa_ai – your personal AI-powered book discovery assistant that not only curates the best reads tailored to your interests but also lets you **chat directly with the AI** to explore book insights in real-time

### 🌟 Why Learnsherpa_ai?

In today's information-rich world, finding the perfect book can feel like searching for a needle in a haystack. Learnsherpa_ai solves this problem by:
- Leveraging AI to analyze thousands of book reviews and ratings
- Providing in-depth, unbiased summaries from various sources
- Real-time chatbot interaction, ask question about what people say in Reddit or in Goodreads about a specific book,and get instant, AI-driven responses.
- Saving you countless hours of research and indecision

## See a demo in action

https://github.com/user-attachments/assets/27d78b53-ad8f-4a91-9508-7179a6507464


### 📊 Example Report

Check out this [example report for Sociology books](./reports/sociology_report_20240903_103808.md) or the [example report for Productivity books](./reports/productivity_report_20240906_113032.md) to see the depth and quality of information Learnsherpa_ai provides.

In each report, you'll find:
- Detailed book summaries
- Goodreads ratings and review summaries
- Reddit discussion highlights
- Direct links to Goodreads book pages and relevant Reddit threads

These links allow you to dive deeper into specific reviews or join ongoing discussions about the books that interest you most.

### 🔍 How It Works
The workflow is illustrated in the following chart:

![Learnsherpa_ai Workflow](img/workflow.png)

Learnsherpa_ai employs a sophisticated crew of AI agents, each specializing in different aspects of book research:
1. **Best Books Researcher**: Identifies top-rated books in your chosen genre
2. **Goodreads Searcher**: Gathers and summarizes reviews from avid readers
3. **Reddit Reviewer**: Finds and analyzes discussions from book communities
4. **Orchestrator**: Compiles all the information into a comprehensive report

### 🚀 Features

- **Genre-specific recommendations**: Get tailored book suggestions for any genre
- **Comprehensive reports**: Receive detailed summaries, ratings, and public opinions
- **Up-to-date information**: Access the latest reviews and discussions
- **Easy-to-use command-line interface**: Generate reports with a simple command
- **Direct links to sources**: Each report includes links to Goodreads reviews and Reddit discussions
- **Real-time chatbot interaction**:  Ask questions about book reviews, ratings, and discussions using a Chainlit-powered chatbot.



### 🛠️ Installation

1. Clone the repository:
   ```
   git clone https://github.com/sosanzma/learnsherpa_ai.git
   cd learnsherpa_ai
   ```

2. Install dependencies using Poetry:
   ```
   poetry lock && poetry install
   ```

3. Configure API keys:
   - Create a `.env` file in the root directory of the project
   - Add your OpenAI and Serper API keys to the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     SERPER_API_KEY=your_serper_api_key_here
     ```
   Make sure to replace `your_openai_api_key_here` and `your_serper_api_key_here` with your actual API keys.

### 📖 Usage

Generate a book recommendation report for any genre using the following command:
```
poetry run learnsherpa_ai "Your Genre"
```

For example:
```
poetry run learnsherpa_ai "Science Fiction"
```

Your report will be generated and saved in the `reports` directory.

### 🌈 Experience the Future of Book Discovery

Don't let another great book pass you by. With Learnsherpa_ai, you're always just one command away from your next literary adventure. Start exploring now and transform the way you discover books forever!

---

📣 I'm constantly improving Learnsherpa_ai. If you have any feedback or suggestions, please open an issue or submit a pull request. Happy reading! 📚
