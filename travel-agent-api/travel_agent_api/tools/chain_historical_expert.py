from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


_model = ChatOpenAI(model="gpt-4o-mini")

_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a historical expert.
Provide in-depth, accurate, and well-structured explanations.
Answer clearly and helpfully."""),
    ("human", "{input}"),
])


_chain = _prompt | _model


@tool
def chain_historical_expert(input_text: str) -> str:
    """
    Tool che utilizza un modello LLM per fornire contenuti storici approfonditi.
    Args:
        input_text (str): Argomento storico.
    Returns:
        str: Contenuto generato dal modello.
    """
    result = _chain.invoke({"input": input_text})

    print("*" * 80)
    print("chain_historical_expert")
    print("*" * 80)

    return result.content