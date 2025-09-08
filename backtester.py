
import pandas as pd
from dataclasses import dataclass
from typing import Dict, Tuple
from ..data_sources.csv_feed import CSVFeed
from ..strategies.steam_chaser import SteamChaser
from ..strategies.mean_reversion import MeanReversion
from ..execution.executor import Executor, Position
from ..risk.risk_manager import RiskManager
from ..utils import odds as u

@dataclass
class TradeResult:
    event_id:str; selection_id:int; entry_odds:float; exit_odds:float; side:str; pnl_win:float; pnl_lose:float; reason:str

class Backtester:
    def __init__(self, data_path:str, strategy:str, params:dict, bank:float, sf:float, cap:float, time_exit_sec:int):
        self.feed=CSVFeed(data_path)
        self.strategy=SteamChaser(**params) if strategy=='steam_chaser' else MeanReversion(**({**params,'time_exit_sec':time_exit_sec}))
        self.exec=Executor(); self.risk=RiskManager(bank,sf,cap)
        self.bank=bank; self.sf=sf; self.exit=time_exit_sec
        self.open:Dict[Tuple[str,int],Position]={}; self.results:list[TradeResult]=[]
    def run(self):
        for row in self.feed.iter_rows():
            k=(row.event_id,row.selection_id)
            if k in self.open and int(row.seconds_to_kickoff)<=self.exit:
                pos=self.open.pop(k); hedge=row.lay_odds if pos.side=='BACK' else row.back_odds
                w,l=self.exec.hedge(pos, hedge, self.bank, self.sf); self.results.append(TradeResult(row.event_id,row.selection_id,pos.entry_odds,pos.exit_odds or 0.0,pos.side,w,l,'time_exit')); self.risk.register_close(row.event_id,pos.stake)
            if k not in self.open:
                sig=self.strategy.on_tick(row)
                if sig and self.risk.can_open(row.event_id):
                    pos=self.exec.open(sig); pos.stake=max(2.0,self.bank*self.sf); self.open[k]=pos; self.risk.register_open(row.event_id,pos.stake)
            else:
                pos=self.open[k]; cur_lay=row.lay_odds; cur_back=row.back_odds
                if pos.side=='BACK':
                    tgt=u.move_ticks(pos.entry_odds,-2); stp=u.move_ticks(pos.entry_odds,3); hit_tp=cur_lay<=tgt; hit_sl=cur_lay>=stp; hedge=cur_lay
                else:
                    tgt=u.move_ticks(pos.entry_odds,2); stp=u.move_ticks(pos.entry_odds,-3); hit_tp=cur_back>=tgt; hit_sl=cur_back<=stp; hedge=cur_back
                if hit_tp or hit_sl:
                    pos=self.open.pop(k); w,l=self.exec.hedge(pos, hedge, self.bank, self.sf); self.results.append(TradeResult(row.event_id,row.selection_id,pos.entry_odds,pos.exit_odds or 0.0,pos.side,w,l,'tp' if hit_tp else 'sl')); self.risk.register_close(row.event_id,pos.stake)
    def report(self)->pd.DataFrame:
        if not self.results: return pd.DataFrame(columns=['event_id','selection_id','side','entry_odds','exit_odds','pnl_win','pnl_lose','reason','pnl_avg'])
        df=pd.DataFrame([r.__dict__ for r in self.results]); df['pnl_avg']=(df['pnl_win']+df['pnl_lose'])/2.0; return df
