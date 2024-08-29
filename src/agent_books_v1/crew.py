import os
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from agent_books_v1.tools.searcher_tool import SearchTools
import sys
sys.path.append('./cursor_agent_books_v1/src')
from crewai_tools import SerperDevTool


# Environment variables for API keys
from dotenv import load_dotenv
load_dotenv()
import yaml

# Uncomment the following line to use an example of a custom tool
# from agent_books_v1.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class AgentBooksV1Crew:
    """AgentBooksV1 crew"""
    
    def __init__(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        print(base_path)
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
    def searcher(self) -> Agent:
        """Searcher agent for finding book recommendations by specified people"""
        return Agent(
            role=self.agents_config['searcher']['role'],
            goal=self.agents_config['searcher']['goal'],
            backstory=self.agents_config['searcher']['backstory'],
            tools=[SerperDevTool()],
            verbose=True,
            llm=self.get_llm('gpt-4o-mini')
        )
    
    @agent
    def best_books_researcher(self) -> Agent:
        """Best Books Researcher agent for finding top-rated books in the genre"""
        return Agent(
            role=self.agents_config['best_books_researcher']['role'],
            goal=self.agents_config['best_books_researcher']['goal'],
            backstory=self.agents_config['best_books_researcher']['backstory'],
            tools=[SerperDevTool()],
            verbose=True,
            llm=self.get_llm('gpt-4o-mini')
        )
    
    @agent
    def reddit_reviewer(self) -> Agent:
        """Reddit Reviewer agent for summarizing Reddit opinions on books"""
        return Agent(
            role=self.agents_config['reddit_reviewer']['role'],
            goal=self.agents_config['reddit_reviewer']['goal'],
            backstory=self.agents_config['reddit_reviewer']['backstory'],
            tools=[SerperDevTool()],
            verbose=True,
            llm=self.get_llm('gpt-4o-mini')
        )

    @agent
    def orchestrator(self) -> Agent:
        """Orchestrator agent for compiling the final report"""
        return Agent(
            role=self.agents_config['orchestrator']['role'],
            goal=self.agents_config['orchestrator']['goal'],
            backstory=self.agents_config['orchestrator']['backstory'],
            verbose=True,
            llm=self.get_llm('gpt-4o-mini')
        )

    @task
    def search_books_task(self) -> Task:
        """Task for the Searcher agent to find book recommendations"""
        return Task(
            description=self.tasks_config['search_books_task']['description'],
            agent=self.searcher(),
            expected_output="A list of book recommendations based on the search criteria"
        )

    @task
    def find_best_books_task(self) -> Task:
        """Task for the Best Books Researcher agent to find top-rated books"""
        return Task(
            description=self.tasks_config['find_best_books_task']['description'],
            agent=self.best_books_researcher(),
            expected_output="A list of top-rated books in the specified genre"
        )

    @task
    def gather_reddit_reviews_task(self) -> Task:
        """Task for the Reddit Reviewer agent to gather and summarize Reddit opinions"""
        return Task(
            description=self.tasks_config['gather_reddit_reviews_task']['description'],
            agent=self.reddit_reviewer(),
            expected_output="A summary of Reddit opinions on the recommended books"
        )

    @task
    def compile_final_report_task(self) -> Task:
        """Task for the Orchestrator agent to compile the final report"""
        return Task(
            description=self.tasks_config['compile_final_report_task']['description'],
            agent=self.orchestrator(),
            context=[self.search_books_task(), self.find_best_books_task(), self.gather_reddit_reviews_task()],
            expected_output="A comprehensive report on book recommendations with insights from various sources"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BookRecommendationCrew crew"""
        return Crew(
            agents=[
                self.searcher(),
                self.best_books_researcher(),
                self.reddit_reviewer(),
                self.orchestrator()
            ],
            tasks=[
                self.search_books_task(),
                self.find_best_books_task(),
                self.gather_reddit_reviews_task(),
                self.compile_final_report_task()
            ],
            process=Process.sequential,
            verbose=True
        )

def run_crew():
    crew_instance = AgentBooksV1Crew()
    result = crew_instance.crew().kickoff(inputs={
        'genre': 'neuroscience',
        'person_1': 'Elon Musk',
        'person_2': 'Mark Zuckerberg',
        'person_3': 'Lex Fridman'
    })
    print(result)

if __name__ == "__main__":
    run_crew()