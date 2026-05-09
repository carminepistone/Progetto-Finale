from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Optional, List


_model = ChatOpenAI(model="gpt-4o-mini")


class TravelDayOutput(BaseModel):
    morning: str
    afternoon: str
    evening: str


class TravelPlanOutput(BaseModel):
    travel_plan: List[TravelDayOutput]


class TravelPlanInput(BaseModel):
    start_date: str = Field(description="The start date (YYYY-MM-DD).")
    end_date: str = Field(description="The end date (YYYY-MM-DD).")
    destination: str = Field(description="The destination of the trip.")
    adults: Optional[int] = Field(1, description="Number of adults.")
    children: Optional[int] = Field(0, description="Number of children.")
    travel_style: str = Field(
        description="Travel style (e.g. adventure, relax, culture)."
    )
    budget: Optional[int] = Field(None, description="Total budget.")
    activities: str = Field(description="Preferred activities.")
    food_restriction: str = Field(description="Food restrictions.")


_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a travel expert. Generate a structured travel plan."),
    ("human", """
Create a travel plan with morning, afternoon, evening for each day.
- start_date: {start_date}
- end_date: {end_date}
- destination: {destination}
- adults: {adults}
- children: {children}
- travel_style: {travel_style}
- budget: {budget}
- activities: {activities}
- food_restriction: {food_restriction}
"""),
])


_chain = _prompt | _model.with_structured_output(TravelPlanOutput)



@tool(args_schema=TravelPlanInput)
def chain_travel_plan(
    start_date: str,
    end_date: str,
    destination: str,
    travel_style: str,
    activities: str,
    food_restriction: str,
    adults: Optional[int] = 1,
    children: Optional[int] = 0,
    budget: Optional[int] = None,
) -> dict:
    """Generates a structured travel plan using an LLM."""
    result: TravelPlanOutput = _chain.invoke({
        "start_date": start_date,
        "end_date": end_date,
        "destination": destination,
        "adults": adults,
        "children": children,
        "travel_style": travel_style,
        "budget": budget,
        "activities": activities,
        "food_restriction": food_restriction,
    })

    print("*" * 80)
    print("chain_travel_plan")
    print("*" * 80)

    return result.model_dump()