
import pandas as pd
REQ = ["timestamp","event_id","selection_id","runner","seconds_to_kickoff","back_odds","lay_odds","traded_volume"]
class CSVFeed:
    def __init__(self, path:str):
        df = pd.read_csv(path)
        for c in REQ:
            if c not in df.columns: raise ValueError(f"Manca colonna: {c}")
        self.df = df.sort_values(['event_id','seconds_to_kickoff'], ascending=[True, False]).reset_index(drop=True)
    def iter_rows(self):
        for r in self.df.itertuples(index=False): yield r
