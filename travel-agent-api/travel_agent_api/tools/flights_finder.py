import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from serpapi import GoogleSearch
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()


class FlightsInput(BaseModel):
    departure_airport: str = Field(description="The departure airport code (IATA).")
    arrival_airport: str = Field(description="The arrival airport code (IATA).")
    outbound_date: str = Field(
        description="The outbound date (YYYY-MM-DD) e.g. 2024-12-13."
    )
    return_date: str = Field(
        description="The return date (YYYY-MM-DD) e.g. 2024-12-19."
    )
    adults: Optional[int] = Field(1, description="The number of adults. Defaults to 1.")
    children: Optional[int] = Field(
        0, description="The number of children. Defaults to 0."
    )



@tool(args_schema=FlightsInput)
def flights_finder(
    departure_airport: str,
    arrival_airport: str,
    outbound_date: str,
    return_date: str,
    adults: Optional[int] = 1,
    children: Optional[int] = 0,
):
    """
    This tool uses the SerpApi Google Flights API to retrieve flights info.
    Parameters:
        departure_airport (str): The departure airport code (IATA).
        arrival_airport (str): The arrival airport code (IATA).
        outbound_date (str): The outbound date (YYYY-MM-DD) e.g. 2024-12-13.
        return_date (str): The return date (YYYY-MM-DD) e.g. 2024-12-19.
        adults (int): The number of adults. Defaults to 1.
        children (int): The number of children. Defaults to 0.
    Returns:
        dict: A dictionary containing the flights info.
              If the API call fails, it returns the error message as a string.
    """
    try:
        query_params = {
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "engine": "google_flights",
            "hl": "it",
            "gl": "it",
            "currency": "EUR",
            "stops": "1",
            "departure_id": departure_airport,
            "arrival_id": arrival_airport,
            "outbound_date": outbound_date,
            "return_date": return_date,
            "adults": adults,
            "children": children,
        }
        search = GoogleSearch(query_params)

        print("*" * 80)
        print("flights_finder")
        print("*" * 80)

        return search.get_dict()

    except Exception as e:
        return str(e)