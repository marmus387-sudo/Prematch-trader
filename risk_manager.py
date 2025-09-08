
class RiskManager:
    def __init__(self, bank:float, stake_fraction:float, max_exposure_per_event:float):
        self.bank=bank; self.sf=stake_fraction; self.cap=max_exposure_per_event; self.exp={}
    def can_open(self, event_id:str)->bool: return self.exp.get(event_id,0.0) < self.cap*self.bank
    def register_open(self, event_id:str, stake:float): self.exp[event_id]=self.exp.get(event_id,0.0)+stake
    def register_close(self, event_id:str, stake:float): self.exp[event_id]=max(0.0, self.exp.get(event_id,0.0)-stake)
