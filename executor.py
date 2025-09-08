
from dataclasses import dataclass
from ..utils import odds as u
@dataclass
class Position: side:str; entry_odds:float; stake:float; hedged:bool=False; exit_odds:float|None=None
class Executor:
    def __init__(self, slippage_ticks:int=1): self.slip=slippage_ticks
    def open(self, sig): 
        eo = u.move_ticks(sig.entry_odds, self.slip if sig.side=='BACK' else -self.slip); 
        return Position(sig.side, eo, 0.0)
    def hedge(self, pos:Position, cur_odds:float, bank:float, stake_fraction:float):
        if pos.stake==0.0: pos.stake=max(2.0, bank*stake_fraction)
        if pos.side=='BACK':
            ls=u.hedge_lay_stake(pos.entry_odds,pos.stake,cur_odds); w,l=u.pnl_from_back_lay(pos.entry_odds,pos.stake,cur_odds,ls)
            pos.hedged=True; pos.exit_odds=cur_odds; return w,l
        else:
            bs=u.hedge_back_stake(pos.entry_odds,pos.stake,cur_odds); liab=pos.stake*(pos.entry_odds-1.0)
            w=pos.stake-bs; l=bs*(cur_odds-1.0)-liab; pos.hedged=True; pos.exit_odds=cur_odds; return w,l
