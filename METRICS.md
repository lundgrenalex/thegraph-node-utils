## Metrics
* count blocks per minute
* estimation day in days
* features

### How to use

#### Install app env
```bash
python3 -m venv .venv
. ./.venv/bin/activate
pip3 install pip --upgrade
pip3 install -r requirements.txt
```

#### Collect data to json file
Before u have to change base url for your indexer inside script `get_get_data_from_indexer.py`.
All data collected to `checks/store.json`.
You can run whis app every N-sec. Example (run every 30min [60sec * 30]):
```bash
watch -n 1800 python3 src/apps/get_get_data_from_indexer.py
```

### Get stats for subgraps from indexer
```bash
python3 src/apps/calc_indexing_status.py
```

Example output:
```bash
Total subgraps count: 22

##### STOPPED SUBGRAPHS ####

Subgraph hash is QmZeu1LAvJ5D827bXiJrHZ6BuwGwVdhY7hL54gAvUXN3Pd
Details:
Synced: False
Head block: 16875266
Latest Block: 15976486
Stored entities: 3721157
Error: handler=None message='Failed to transact block operations: subgraph writer poisoned by previous error' block_number=15976240
Sync speed blocks/per min: None
Estimation time to sync all blocks: None days

Subgraph hash is QmaYtSbktWsvxB8YJmtUTfzrQJrzZtF2oMoiVkn3pq64D9
Details:
Synced: False
Head block: 16875266
Latest Block: 11367731
Stored entities: 158112
Error: handler=None message='Failed to transact block operations: subgraph writer poisoned by previous error' block_number=11356225
Sync speed blocks/per min: None
Estimation time to sync all blocks: None days

##### UNHEALTHY SUBGRAPHS ####

None

##### SYNCED SUBGRAPHS ####

Subgraph hash is QmTFA73btdBWDMC9PymE3xGiBEDfrfPjeRWQ1X47EMTdCU
Details:
Synced: True
Head block: 16875266
Latest Block: 16875266
Stored entities: 74
Error: None
Sync speed blocks/per min: 4.0
Estimation time to sync all blocks: 2439 days

Subgraph hash is QmRBf4UKMGh8PTa6TKfjK6SrGoLF48H9tCx1aBmHHJNYkM
Details:
Synced: True
Head block: 16875266
Latest Block: 16875266
Stored entities: 373942
Error: None
Sync speed blocks/per min: 4.0
Estimation time to sync all blocks: 2440 days

##### SYNCING SUBGRAPHS ####

Subgraph hash is QmfGbT45D97qwe65CjHeqJ39w3h6JRPBeCFxe1ztSnAcZE
Details:
Synced: False
Head block: 16875266
Latest Block: 12042625
Stored entities: 4413977
Error: None
Sync speed blocks/per min: 250.0
Estimation time to sync all blocks: 46 days

Subgraph hash is QmQiNQfyJYV6A9MZ8p7Um8ksoKLXTw2rQAM1QzokFCBhp7
Details:
Synced: False
Head block: 16875266
Latest Block: 12329657
Stored entities: 107651
Error: None
Sync speed blocks/per min: 2786.0
Estimation time to sync all blocks: 3 days
```