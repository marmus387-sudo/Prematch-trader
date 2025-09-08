
from dataclasses import dataclass
from collections import deque
from statistics import fmean, pstdev
from ..utils.odds import move_ticks
@dataclass
class Signal: side:str; entry_odds:float; target_odds:float; stop_odds:float; reason:str
class MeanReversion:
    def __init__(self, window=900, z_entry=2.0, target_ticks=2, stop_ticks=4, time_exit_sec=600):
        self.w=window; self.z=z_entry; self.tt=target_ticks; self.st=stop_ticks; self.exit=time_exit_sec; self.buf={}
    def _b(self,k):
        if k not in self.buf: self.buf[k]=deque()
        return self.buf[k]
    def on_tick(self,row):
        k=(row.event_id,row.selection_id); b=self._b(k); st=int(row.seconds_to_kickoff)
        b.append((st,row.lay_odds))
        while b and b[0][0]-st>self.w: b.popleft()
        lays=[x[1] for x in b]
        if len(lays)<10 or st<=self.exit: return None
        mu=fmean(lays); sd=pstdev(lays) or 1e-9; z=(row.lay_odds-mu)/sd
        if z>=self.z:
            e=row.lay_odds; return Signal("BACK", e, move_ticks(e,-self.tt), move_ticks(e,self.st), f"z={z:.2f}")
        if z<=-self.z:
            e=row.back_odds; return Signal("LAY", e, move_ticks(e,self.tt), move_ticks(e,-self.st), f"z={z:.2f}")
        return None
