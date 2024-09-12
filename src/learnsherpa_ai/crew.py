import os
from crewai import Agent, Task, Crew, Process
from crewai.crews.crew_output import CrewOutput
from crewai.project import CrewBase, agent, crew, task
from learnsherpa_ai.tools.searcher_tool import SearchTools
import sys
sys.path.append('./learnsherpa_ai/src')
from crewai_tools import SerperDevTool


# Environment variables for API keys
from dotenv import load_dotenv
load_dotenv()
import yaml



# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool
@CrewBase
class AgentBooksV1Crew:
    """AgentBooksV1 Crew"""
    
    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.agents_config = self.load_config(os.path.join(base_path, 'config', 'agents.yaml'))
        self.tasks_config = self.load_config(os.path.join(base_path, 'config', 'tasks.yaml'))

    def load_config(self, path):
        with open(path, 'r') as file:
            return yaml.safe_load(file)

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

    @agent
    def best_books_researcher(self) -> Agent:
        """Best Books Researcher agent for finding top-rated books in the genre"""
        return Agent(
            role=self.agents_config['best_books_researcher']['role'],
            goal=self.agents_config['best_books_researcher']['goal'],
            backstory=self.agents_config['best_books_researcher']['backstory'],
            tools=[SerperDevTool()],
            verbose=False,
            allow_delegation=False,
            llm=self.get_llm('gpt-4o-2024-08-06')
        )
        
    @agent
    def searcher_goodreads(self) -> Agent:
        """Searcher agent for finding book opinions on Goodreads"""
        return Agent(
            role=self.agents_config['searcher_goodreads']['role'],
            goal=self.agents_config['searcher_goodreads']['goal'],
            backstory=self.agents_config['searcher_goodreads']['backstory'],
            tools=[SerperDevTool()],
            verbose=False,
            llm=self.get_llm('gpt-4o-2024-08-06')
        )
    
    @agent
    def reddit_reviewer(self) -> Agent:
        """Reddit Reviewer agent for summarizing Reddit opinions on books"""
        return Agent(
            role=self.agents_config['reddit_reviewer']['role'],
            goal=self.agents_config['reddit_reviewer']['goal'],
            backstory=self.agents_config['reddit_reviewer']['backstory'],
            tools=[SerperDevTool()],
            verbose=False,
            llm=self.get_llm('gpt-4o-mini')
        )

    @agent
    def orchestrator(self) -> Agent:
        """Orchestrator agent for compiling the final report"""
        return Agent(
            role=self.agents_config['orchestrator']['role'],
            goal=self.agents_config['orchestrator']['goal'],
            backstory=self.agents_config['orchestrator']['backstory'],
            verbose=False,
            llm=self.get_llm('gpt-4o-mini')
        )

    @task
    def find_best_books_task(self) -> Task:
        """Task for the Best Books Researcher agent to find top-rated books"""
        return Task(
            description=self.tasks_config['find_best_books_task']['description'],
            agent=self.best_books_researcher(),
            expected_output=self.tasks_config['find_best_books_task']['expected_output'],
        )

    @task
    def gather_goodreads_reviews_task(self) -> Task:
        """Task for the searcher_goodreads agent to find book reviews from people"""
        return Task(
            description=self.tasks_config['gather_goodreads_reviews_task']['description'],
            agent=self.searcher_goodreads(),
            context=[self.find_best_books_task()],
            expected_output=self.tasks_config['gather_goodreads_reviews_task']['expected_output'],
        )
    
    @task
    def gather_reddit_reviews_task(self) -> Task:
        """Task for the Reddit Reviewer agent to gather and summarize Reddit opinions"""
        return Task(
            description=self.tasks_config['gather_reddit_reviews_task']['description'],
            agent=self.reddit_reviewer(),
            context=[self.find_best_books_task()],
            expected_output=self.tasks_config['gather_reddit_reviews_task']['expected_output'],
        )

    @task
    def compile_final_report_task(self) -> Task:
        """Task for the Orchestrator agent to compile the final report"""
        return Task(
            description=self.tasks_config['compile_final_report_task']['description'],
            agent=self.orchestrator(),
            context=[self.gather_goodreads_reviews_task(), self.find_best_books_task(), self.gather_reddit_reviews_task()],
            expected_output=self.tasks_config['compile_final_report_task']['expected_output'],
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the BookRecommendationCrew crew"""
        return Crew(
            agents=[
                self.best_books_researcher(),
                self.searcher_goodreads(),
                self.reddit_reviewer(),
                self.orchestrator()
            ],
            tasks=[
                self.find_best_books_task(),
                self.gather_goodreads_reviews_task(),
                self.gather_reddit_reviews_task(),
                self.compile_final_report_task()
            ],
            process=Process.sequential,
            verbose=True
        )

    def save_reports(self, crew_output: CrewOutput):
        """Save the reports generated by the agents"""
        print("token usage : ", crew_output.token_usage)
                # Save the outputs from each task execution
        for i, task_output in enumerate(crew_output.tasks_output, start=1):
            print(task_output)
            if task_output.agent == "Book Recommendation Searcher":
                path = f'tmp_reports/goodreads_report.txt'
            elif task_output.agent == "Public Opinion Analyst":
                path = f'tmp_reports/reddit_report.txt'
            else:
                continue  # Skip other tasks not related to reports
            
            with open(path, 'w') as file:
                file.write(str(task_output))
                print(f"Saved output to {path}")

