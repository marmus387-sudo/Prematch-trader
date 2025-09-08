
import hmac, hashlib, os
def _mac(user, plan, secret): return hmac.new(secret.encode(), f"{user}|{plan}".encode(), hashlib.sha256).hexdigest()[:16]
def valid_license(key:str, secret:str)->bool:
    try: user, plan, sig = key.split("|")
    except ValueError: return False
    return hmac.compare_digest(_mac(user,plan,secret), sig)
def require_license():
    if os.getenv("LICENSE_ENFORCE","1")!="1": return
    secret=os.getenv("LICENSE_SECRET",""); key=os.getenv("LICENSE_KEY","")
    if not secret or not key or not valid_license(key, secret): raise SystemExit("Licenza non valida o mancante.")
