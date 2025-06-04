import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from .ledger import ProgressLedger, LedgerEntry

class Executor:
    def __init__(self, manifest_path: Path, protocol_path: Path, ledger_path: Path):
        self.manifest = json.loads(manifest_path.read_text())
        self.protocol = json.loads(protocol_path.read_text())
        self.ledger = ProgressLedger(ledger_path)

    def run(self):
        for step_id in self.manifest.get("macro_order", []):
            task = next(t for t in self.manifest["tasks"] if t["id"] == step_id)
            status = self.ledger.last_status(step_id)
            if status == "Complete":
                continue
            result = self.execute_step(task)
            entry = LedgerEntry(
                step_id=step_id,
                ts=datetime.utcnow().isoformat() + "Z",
                status="Complete" if result["returncode"] == 0 else "Errored",
                artifacts={"stdout": result["stdout"], "stderr": result["stderr"]}
            )
            self.ledger.append(entry)

    def execute_step(self, task: Dict[str, Any]) -> Dict[str, Any]:
        command = task.get("command")
        if not command:
            return {"returncode": 0, "stdout": "", "stderr": ""}
        proc = subprocess.run(command, shell=True, capture_output=True, text=True)
        return {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest")
    parser.add_argument("protocol")
    parser.add_argument("ledger", default="progress.json")
    args = parser.parse_args()

    executor = Executor(Path(args.manifest), Path(args.protocol), Path(args.ledger))
    executor.run()
