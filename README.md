# Manifest Protocol Progress Example

This repository demonstrates a minimal implementation of the Manifest → Protocol → Progress concept. A simple executor reads a manifest and protocol, executes each task, and records progress in a ledger.

## Files

- `manifest.json` – example manifest describing tasks.
- `protocol.json` – protocol configuration.
- `progress.json` – ledger created during execution.
- `app/` – Python modules implementing the executor and ledger.

## Running

Execute the manifest using Python 3:

```bash
python -m app.executor manifest.json protocol.json progress.json
```

After running, `progress.json` will contain the results for each step.
