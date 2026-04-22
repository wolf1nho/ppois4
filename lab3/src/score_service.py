import datetime
import json


class ScoreService:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                raw = f.read().strip()
            if not raw:
                return []

            if raw.isdigit():
                legacy_score = int(raw)
                if legacy_score <= 0:
                    return []
                now = datetime.datetime.now()
                return [
                    {
                        "name": "Legacy",
                        "score": legacy_score,
                        "date": now.strftime("%Y-%m-%d"),
                        "time": now.strftime("%H:%M:%S"),
                    }
                ]

            data = json.loads(raw)
            if not isinstance(data, list):
                return []

            clean = []
            for entry in data:
                if not isinstance(entry, dict):
                    continue
                name = str(entry.get("name", "Player"))[:20].strip() or "Player"
                score = int(entry.get("score", 0))
                date = str(entry.get("date", "---- -- --"))
                tm = str(entry.get("time", "--:--:--"))
                clean.append({"name": name, "score": score, "date": date, "time": tm})

            clean.sort(key=lambda x: x["score"], reverse=True)
            return clean[:10]
        except Exception:
            return []

    def save(self, highscores):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(highscores[:10], f, ensure_ascii=False, indent=2)

    def add_record(self, highscores, name, score):
        now = datetime.datetime.now()
        record = {
            "name": (name.strip() or "Player")[:20],
            "score": int(score),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
        }
        updated = list(highscores)
        updated.append(record)
        updated.sort(key=lambda x: x["score"], reverse=True)
        return updated[:10]
