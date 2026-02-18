from app.core.llm import get_llm
from app.tools.registry import TOOLS
from app.agents.agent import Agent

def main():
    llm = get_llm()
    agent = Agent(llm=llm, tools=TOOLS)

    user_input = input("Ask something: ")
    result = agent.run(user_input)

    print("\nFinal Answer:")
    print(result.model_dump())

if __name__ == "__main__":
    main()