class Metrics:
    def log(self, event:str, data:dict):
        print(f"[METRICS] {event} | {data}")