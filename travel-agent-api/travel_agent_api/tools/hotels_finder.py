import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from serpapi import GoogleSearch
from pydantic import BaseModel, Field
from typing import Optional
from enum import IntEnum

load_dotenv()


class HotelClassEnum(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class HotelsInput(BaseModel):
    q: str = Field(description="Location of the hotel.")
    check_in_date: str = Field(
        description="The check-in date (YYYY-MM-DD) e.g. 2024-12-13."
    )
    check_out_date: str = Field(
        description="The check-out date (YYYY-MM-DD) e.g. 2024-12-19."
    )
    adults: Optional[int] = Field(1, description="The number of adults. Defaults to 1.")
    children: Optional[int] = Field(
        0, description="The number of children. Defaults to 0."
    )
    hotel_class: Optional[HotelClassEnum] = Field(
        HotelClassEnum.TWO,
        description="The hotel class available from 2 to 5.",
    )


@tool(args_schema=HotelsInput)
def hotels_finder(
    q: str,
    check_in_date: str,
    check_out_date: str,
    adults: Optional[int] = 1,
    children: Optional[int] = 0,
    hotel_class: Optional[HotelClassEnum] = HotelClassEnum.TWO,
):
    """
    This tool uses the SerpApi Google Hotels API to retrieve hotels info.
    """
    try:
        query_params = {
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "engine": "google_hotels",
            "hl": "it",
            "gl": "it",
            "currency": "EUR",
            "q": q,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "adults": adults,
            "children": children,
            "hotel_class": int(hotel_class) if hotel_class is not None else 2,
            "num": 5,
        }
        search = GoogleSearch(query_params)
        results = search.get_dict().get("properties", [])

        print("*" * 80)
        print("hotels_finder")
        print("*" * 80)

        return results

    except Exception as e:
        print("Error:", e)
        return str(e)