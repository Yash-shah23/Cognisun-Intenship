from crewai import Agent, Task, Crew
from langchain_ollama import Ollama  # ✅ this is the correct modern one

def get_crew_agent():
    llm = Ollama(model="gemma:2b")

    agent = Agent(
        role="Helpful Assistant",
        goal="Answer user questions clearly and informatively",
        backstory="You are an intelligent assistant helping users with clear and concise answers.",
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )

    task = Task(
        description="Answer the user's question in a helpful and accurate way.",
        expected_output="A clear and informative answer to the user's question.",
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )

    return crew
