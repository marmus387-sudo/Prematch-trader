
from dataclasses import dataclass
from collections import deque
from ..utils.odds import move_ticks
@dataclass
class Signal: side:str; entry_odds:float; target_odds:float; stop_odds:float; reason:str
class SteamChaser:
    def __init__(self, momentum_ticks=3, momentum_window_sec=900, target_ticks=2, stop_ticks=3, min_volume_ratio=1.3, time_exit_sec=600):
        self.ticks=momentum_ticks; self.win=momentum_window_sec; self.tt=target_ticks; self.st=stop_ticks; self.vr=min_volume_ratio; self.exit=time_exit_sec; self.buf={}
    def _b(self,k): 
        if k not in self.buf: self.buf[k]={"w":deque()}; 
        return self.buf[k]
    def on_tick(self,row):
        k=(row.event_id,row.selection_id); b=self._b(k); st=int(row.seconds_to_kickoff)
        b["w"].append((st,row.back_odds,row.lay_odds,row.traded_volume))
        while b["w"] and b["w"][0][0]-st>self.win: b["w"].popleft()
        lays=[x[2] for x in b["w"]]
        if len(lays)<2 or st<=self.exit: return None
        max_lay=max(lays); cur=row.lay_odds
        # pseudo: se sceso almeno N tick (approssimazione con differenza assoluta)
        drop = 1 if cur < max_lay else 0
        # volume check (semplificato)
        if drop and True:
            entry=cur; target=move_ticks(entry, -self.tt); stop=move_ticks(entry, self.st)
            return Signal("BACK", entry, target, stop, "steam")
        return None
