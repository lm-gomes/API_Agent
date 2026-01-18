from fastapi import FastAPI
import httpx
from agent.agent import prompt_to_agent
app = FastAPI()



@app.post("/agent")
async def agent_endpoint(data: dict):
    return await prompt_to_agent(data)



@app.post("/prompt")
async def send_first_message():
    data = {"message":"minha internet ta caindo o tempo todo, sabe o que pode ser?", "summary": "O usuário se apresentou como Jorge."}
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post("http://app:8000/agent", json=data)
        return r.json()

