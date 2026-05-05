from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from travel_agent_api.services.agent_service import Agent

router = APIRouter()

class ChatCompletionRequest(BaseModel):
    messages: list
    model_config = {
        "json_schema_extra": {
            "example": {
                "messages": [
                    {
                        "role": "user",
                        "content": "Vorrei organizzare un viaggio a Roma"
                    }
                ]
            }
        }
    }

@router.post("/travel-agent")
def chat_completion(request: ChatCompletionRequest):
    agent = Agent()

    try:
        message = agent.run(messages=request.messages)
    except RuntimeError as e:
        error_msg = str(e)
        if "Connection error" in error_msg:
            raise HTTPException(
                status_code=503,
                detail="Servizio OpenAI non raggiungibile."
            )
        raise HTTPException(status_code=500, detail=error_msg)

    print("*" * 80)
    print("chat_completion")
    print("*" * 80)


    return {
        "type": "ai",
        "content": message.content
    }