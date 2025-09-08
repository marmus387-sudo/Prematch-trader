
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import subprocess, os
app = FastAPI(title="Prematch Trader API")
API_KEY=os.getenv("API_KEY","changeme")
def check(k):
    if k!=API_KEY: raise HTTPException(status_code=401, detail="Invalid API key")
class Req(BaseModel):
    strategy:str="steam_chaser"; data_path:str="data/sample_data.csv"
@app.get("/healthz") 
def health(): return {"ok":True}
@app.post("/backtest")
def backtest(req:Req, x_api_key: str|None=Header(None)):
    check(x_api_key)
    out = subprocess.check_output(["prematch-trader","backtest","--strategy",req.strategy,"--data",req.data_path], text=True)
    return {"output": out}
