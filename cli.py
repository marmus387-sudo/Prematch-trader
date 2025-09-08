
import argparse, yaml
from .backtest.backtester import Backtester
from .licensing import require_license
def main():
    require_license()
    p=argparse.ArgumentParser(description="Prematch Trader")
    sub=p.add_subparsers(dest="cmd")
    b=sub.add_parser("backtest"); b.add_argument("--data", required=True); b.add_argument("--strategy", choices=["steam_chaser","mean_reversion"], default="steam_chaser")
    pr=sub.add_parser("paper"); pr.add_argument("--data", required=True); pr.add_argument("--strategy", choices=["steam_chaser","mean_reversion"], default="steam_chaser")
    a=p.parse_args()
    with open("prematch_trader/config.yaml","r") as f: cfg=yaml.safe_load(f)
    if a.cmd in ["backtest","paper"]:
        bt=Backtester(a.data, a.strategy, cfg.get("strategy",{}).get("params",{}), cfg["risk"]["bank"], cfg["risk"]["stake_fraction"], cfg["risk"]["max_exposure_per_event"], cfg["strategy"]["params"]["time_exit_sec"])
        bt.run(); rep=bt.report(); print(rep.to_string(index=False)); print("\nTotale trade:", len(rep)); 
        if len(rep): print("P&L totale:", round(rep['pnl_avg'].sum(),2))
    else:
        p.print_help()
