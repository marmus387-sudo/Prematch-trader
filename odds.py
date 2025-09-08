
def tick_size(odds: float) -> float:
    ranges = [(1.01,2.0,0.01),(2.0,3.0,0.02),(3.0,4.0,0.05),(4.0,6.0,0.1),(6.0,10.0,0.2),
              (10.0,20.0,0.5),(20.0,30.0,1.0),(30.0,50.0,2.0),(50.0,100.0,5.0),(100.0,1000.0,10.0)]
    for lo, hi, ts in ranges:
        if lo <= odds < hi: return ts
    return 10.0

def move_ticks(odds: float, ticks: int) -> float:
    cur = odds; step = 1 if ticks>=0 else -1
    for _ in range(abs(ticks)): cur = round(cur + step*tick_size(cur), 5)
    return cur

def hedge_lay_stake(back_odds, back_stake, lay_odds): return back_stake*back_odds/lay_odds
def hedge_back_stake(lay_odds, lay_stake, back_odds): return lay_stake*lay_odds/back_odds
def pnl_from_back_lay(back_odds, back_stake, lay_odds, lay_stake):
    lay_liability = lay_stake*(lay_odds-1.0); p_win = back_stake*(back_odds-1.0) - lay_liability; p_lose = lay_stake - back_stake
    return p_win, p_lose
