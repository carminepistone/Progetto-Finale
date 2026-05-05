from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional, List


class TravelPlanInput(BaseModel):
    start_date: str = Field(description="The start date (YYYY-MM-DD).")
    end_date: str = Field(description="The end date (YYYY-MM-DD).")
    destination: str = Field(description="The destination of the trip.")
    adults: Optional[int] = Field(1, description="Number of adults.")
    children: Optional[int] = Field(0, description="Number of children.")
    travel_style: str = Field(description="Travel style (e.g. adventure, relax, culture).")
    budget: Optional[int] = Field(None, description="Total budget.")
    activities: str = Field(description="Preferred activities.")
    food_restriction: str = Field(description="Food restrictions.")


class TravelDayOutput(BaseModel):
    morning: str
    afternoon: str
    evening: str


class TravelPlanOutput(BaseModel):
    travel_plan: List[TravelDayOutput]


class TravelPlanInputSchema(BaseModel):
    params: TravelPlanInput


@tool(args_schema=TravelPlanInputSchema)
def chain_travel_plan(params: TravelPlanInput) -> dict:
    """Generates a structured travel plan using an LLM."""
    
    
    model = ChatOpenAI(model="gpt-4o-mini").with_structured_output(TravelPlanOutput)

    prompt = ChatPromptTemplate.from_messages([
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
""")
    ])

    chain = prompt | model

    result: TravelPlanOutput = chain.invoke({
        "start_date": params.start_date,
        "end_date": params.end_date,
        "destination": params.destination,
        "adults": params.adults,
        "children": params.children,
        "travel_style": params.travel_style,
        "budget": params.budget,
        "activities": params.activities,
        "food_restriction": params.food_restriction,
    })

    print("*" * 80)
    print("chain_travel_plan")
    print("*" * 80)

    return result.model_dump()