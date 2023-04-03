## UTILS

### Get graphman's list rewind commands for failed subgraphs
__HOWTO:__
```shell
python3 src/apps/rewind_broken_subgraphs.py

graphman rewind 0xaecad5409a963d2dbac66fb6d689dd41d7fc9afd8ac92ac0791e047115240200 16739300 QmfGbT45D97qwe65CjHeqJ39w3h6JRPBeCFxe1ztSnAcZE
graphman rewind 0x6ad3682a462ff682893b1ba4f591a5d9e6d68701d035b5efea0c4a73e80f6b70 16919676 Qmca1arSe9U94sHVpzzdUKizNyqFddsXnBZYqkALmSdSRE
graphman rewind 0xbc9e786dade383731f16dd6ec490cc066685a8cb1c9bfe6302d523ed37f9f57b 16919690 QmWn6By6bzfJfso46GkZjYKKFq9F6bdBYBxhZSq6dW59yj
graphman rewind 0xbc9e786dade383731f16dd6ec490cc066685a8cb1c9bfe6302d523ed37f9f57b 16919690 QmReiqqi2MVv2egSdFDCTbjKgBkFBkTmM9YyqYqqpfzFET
graphman rewind 0xdf1af43e385fa28a68839a20eac36073a30f3e6286dec1f22f158cbc7b8fde68 11415005 QmQgmUrUKBkQfsKdNNnfcUpUxRvyrX27W4knuhn4q6GfpH
graphman rewind 0x6ad3682a462ff682893b1ba4f591a5d9e6d68701d035b5efea0c4a73e80f6b70 16919676 QmP55LkwgbGcDPy8SsVuDFS473mJQrWDgPvCJgNg8EEB8n
graphman rewind 0x6ad3682a462ff682893b1ba4f591a5d9e6d68701d035b5efea0c4a73e80f6b70 16919676 QmaeLDGxWZyckB6o2QsQ1cnMT7bkYCNjRp4F4fZdbb543N
graphman rewind 0xbc9e786dade383731f16dd6ec490cc066685a8cb1c9bfe6302d523ed37f9f57b 16919690 QmS5nZTUZtqxFsjkocqQMAh4fDegGu8yEVmzBTt6ndU24q
graphman rewind 0xc2abba30b0ffd0b3edb99729c7175a9c1c915a34445ded42846925e223d4cd80 16919691 QmYPh4BHfJRszYBP7tnPFPHpKf2DdyHAtgRbE8PAnU1fZN
graphman rewind 0x0a44dc2ded531dacf6dc0c14d9e25939ac52c9c51628a0d13d2d90470b504b21 13610831 QmZRnLHdYZDVU3CP5DXzLF5GGyxEg5uz6kXRG5FateiqQH
```

### Get subgraph info
__HOWTO:__
```shell
python3 src/apps/get_subgraph_info.py QmYPh4BHfJRszYBP7tnPFPHpKf2DdyHAtgRbE8PAnU1fZN
```

Response:
```json
{
    "name": "XXX",
    "health": "failed",
    "synced": false,
    "hash": "QmQSRqdKo7EUUPccofin5NMCRsfbN7gwyzMhikhyFPUMXV",
    "node": null,
    "network": "mainnet",
    "head_block": 16941043,
    "latest_block": 13000000,
    "entities": 9437894,
    "error": {
        "handler": "",
        "message": "",
        "block_number": 0,
        "block_hash": ""
    },
    "features": [
        "nonFatalErrors", "grafting"
    ]
}
```

# Deploy existing subgraph with known ipfs hash
```shell
python3 src/apps/deploy_subgraph_with_ipfs_hash.py my_subgraph_proto_v1 QmYPh4BHfJRszYBP7tnPFPHpKf2DdyHAtgRbE8PAnU1fZN
```