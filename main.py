from app.core.llm import get_llm
from app.schemas.task_response import TaskResponse

def run():
    llm = get_llm()

    messages = [
        {"role": "system", "content": "Return ONLY valid JSON with keys: task_type, confidence, answer"},
        {"role": "user", "content": "What is 2 + 2?"}
    ]

    result = llm.structured_chat(messages, TaskResponse)

    print("\nValidated Object:\n", result)
    print("\nAs Dict:\n", result.model_dump())


if __name__ == "__main__":
    run()