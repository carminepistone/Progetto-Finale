from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


@tool
def chain_historical_expert(input_text: str) -> str:
    """
    Tool che utilizza un modello LLM per fornire contenuti storici approfonditi.

    Args:
        input_text (str): Argomento storico.

    Returns:
        str: Contenuto generato dal modello.
    """

    model = ChatOpenAI(model="gpt-4o-mini")

    system_prompt = """
You are a historical expert.
Provide in-depth, accurate, and well-structured explanations.
Answer clearly and helpfully.
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", "{system_prompt}"),
        ("human", "{input}")
    ])

    chain = prompt | model

    result = chain.invoke({
        "input": input_text,
        "system_prompt": system_prompt
    })

    # Tracing
    print("*" * 80)
    print("chain_historical_expert")
    print("*" * 80)

    return result.content