import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

@dataclass
class LedgerEntry:
    step_id: str
    ts: str
    status: str
    artifacts: Optional[Dict] = None

class ProgressLedger:
    def __init__(self, path: Path):
        self.path = path
        self.entries: List[LedgerEntry] = []
        if path.exists():
            self._load()

    def _load(self):
        data = json.loads(self.path.read_text())
        for entry in data:
            self.entries.append(LedgerEntry(**entry))

    def append(self, entry: LedgerEntry):
        self.entries.append(entry)
        self._save()

    def _save(self):
        self.path.write_text(json.dumps([asdict(e) for e in self.entries], indent=2))

    def last_status(self, step_id: str) -> Optional[str]:
        for e in reversed(self.entries):
            if e.step_id == step_id:
                return e.status
        return None
