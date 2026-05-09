from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langgraph.prebuilt import create_react_agent
from travel_agent_api.tools.flights_finder import flights_finder
from travel_agent_api.tools.hotels_finder import hotels_finder
from travel_agent_api.tools.chain_historical_expert import chain_historical_expert
from travel_agent_api.tools.chain_travel_plan import chain_travel_plan

SYSTEM_PROMPT_TEMPLATE = """
Sei un travel planner esperto. Il tuo compito è organizzare viaggi completi per l'utente.
Usa emoji per migliorare la leggibilità delle risposte.
Data e ora attuale: {current_datetime}
Linee guida per l'output:
- Voli: mostra compagnia, date, orari e durata in formato markdown.
- Hotel: mostra nome, descrizione, prezzo per notte e valutazione in formato markdown.
- Itinerario: organizza per giorno con mattina, pomeriggio e sera in formato markdown.
"""

MAX_HISTORY = 10


ROLE_MAP = {
    "human": "user",
    "ai": "assistant",
    "user": "user",
    "assistant": "assistant",
    "system": "system",
}


class Agent:
    def __init__(self):
        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            timeout=60,
            max_retries=1,
        )
        self.tools = [
            chain_historical_expert,
            flights_finder,
            hotels_finder,
            chain_travel_plan,
        ]
        self.agent_executor = create_react_agent(
            self.model,
            self.tools,
        )

    def _normalize_messages(self, messages: list) -> list:
        """
        Converte i messaggi dal formato Livewire al formato LangChain.

        Livewire manda:  {"type": "human", "content": "..."}
                         {"type": "ai",    "content": "..."}

        LangChain vuole: {"role": "user",      "content": "..."}
                         {"role": "assistant", "content": "..."}
        """
        normalized = []
        for msg in messages:
            role_raw = msg.get("role") or msg.get("type") or "user"
            role = ROLE_MAP.get(role_raw, "user")
            content = msg.get("content", "")


            if not content:
                continue

            normalized.append({"role": role, "content": content})
        return normalized

    def run(self, messages: list) -> AIMessage:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            current_datetime=current_datetime
        )


        normalized = self._normalize_messages(messages)

        conversation_history = [
            {"role": "system", "content": system_prompt}
        ] + normalized

        if len(conversation_history) > MAX_HISTORY + 1:
            conversation_history = (
                conversation_history[:1] + conversation_history[-MAX_HISTORY:]
            )

        try:
            response = self.agent_executor.invoke(
                {"messages": conversation_history},
                config={"recursion_limit": 10},
            )
        except Exception as e:
            raise RuntimeError(f"Agent execution failed: {e}") from e

        return response["messages"][-1]