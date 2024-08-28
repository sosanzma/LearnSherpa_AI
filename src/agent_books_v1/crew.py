import os
from crewai import Agent, Task, Crew, Process
from crewai.base import CrewBase, agent, task, crew
from tools import searcher_tool, book_review_tool, RedditOpinionSearch  # Importing the tools
# Environment variables for API keys
from dotenv import load_dotenv
load_dotenv()

# Uncomment the following line to use an example of a custom tool
# from agent_books_v1.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class AgentBooksV1Crew():
	"""AgentBooksV1 crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def searcher(self) -> Agent:
		"""Searcher agent for finding book recommendations by specified people"""
		return Agent(
			config=self.agents_config['searcher'],
			tools=[searcher_tool],
			verbose=True,
			llm=self.get_llm('gpt-4o-mini')  # Specify the LLM for this agent
		)

	@agent
	def best_books_researcher(self) -> Agent:
		"""Best Books Researcher agent for finding top-rated books in the genre"""
		return Agent(
			config=self.agents_config['best_books_researcher'],
			tools=[book_review_tool],
			verbose=True,
			llm=self.get_llm('gpt-4o-mini')  # Specify the LLM for this agent
		)

	@agent
	def reddit_reviewer(self) -> Agent:
		"""Reddit Reviewer agent for summarizing Reddit opinions on books"""
		return Agent(
			config=self.agents_config['reddit_reviewer'],
			tools=[RedditOpinionSearch],
			verbose=True,
			llm=self.get_llm('gpt-4o-mini')  # Specify the LLM for this agent
		)

	@agent
	def orchestrator(self) -> Agent:
		"""Orchestrator agent for compiling the final report"""
		return Agent(
			config=self.agents_config['orchestrator'],
			verbose=True,
			llm=self.get_llm('gpt-4o-mini')  # Specify the LLM for this agent
		)

	def get_llm(self, model_name):
		"""Helper method to get the LLM based on the model name"""
		if model_name.startswith('gpt'):
			from langchain.chat_models import ChatOpenAI
			return ChatOpenAI(model_name=model_name)
		elif model_name.startswith('claude'):
			from langchain.chat_models import ChatAnthropic
			return ChatAnthropic(model=model_name)
		else:
			raise ValueError(f"Unsupported model: {model_name}")

	@task
	def search_books_task(self) -> Task:
		"""Task for the Searcher agent to find book recommendations"""
		return Task(
			config=self.tasks_config['search_books_task'],
			agent=self.searcher
		)

	@task
	def find_best_books_task(self) -> Task:
		"""Task for the Best Books Researcher agent to find top-rated books"""
		return Task(
			config=self.tasks_config['find_best_books_task'],
			agent=self.best_books_researcher
		)

	@task
	def gather_reddit_reviews_task(self) -> Task:
		"""Task for the Reddit Reviewer agent to gather and summarize Reddit opinions"""
		return Task(
			config=self.tasks_config['gather_reddit_reviews_task'],
			agent=self.reddit_reviewer
		)

	@task
	def compile_final_report_task(self) -> Task:
		"""Task for the Orchestrator agent to compile the final report"""
		return Task(
			config=self.tasks_config['compile_final_report_task'],
			agent=self.orchestrator,
			inputs={
				'search_results': self.search_books_task,
				'best_books': self.find_best_books_task,
				'reddit_reviews': self.gather_reddit_reviews_task
			},
			output_file='book_recommendations_report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the BookRecommendationCrew crew"""
		return Crew(
			agents=self.agents,  # Automatically created by the @agent decorator
			tasks=self.tasks,    # Automatically created by the @task decorator
			process=Process.sequential,  # Sequential process
			verbose=True
		)

# Example of running the crew
if __name__ == "__main__":
	crew_instance = AgentBooksV1Crew()
	result = crew_instance.crew.kickoff(inputs={
		'genre': 'neuroscience',
		'person_1': 'Elon Musk',
		'person_2': 'Mark Zuckerberg',
		'person_3': 'Lex Fridman'
	})
	print(result)