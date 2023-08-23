![unittest](https://github.com/dineshpinto/synchronous-gossip-protocol/actions/workflows/unittest.yml/badge.svg)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)

# synchronous-gossip-protocol

Python implementation of a synchronous gossip protocol. 

```mermaid
flowchart TD
    GossipProtocolParams --> NodeGenerator;
    NodeGenerator -- list --> NonSampleNode;
    NodeGenerator -- list --> SampleNode;
    SampleNode --> Nodes;
    NonSampleNode --> Nodes;
    Nodes --> NetworkState;
    subgraph NetworkState
        NodeState --> StateTransitionFunction
        StateTransitionFunction --> NodeState;
    end
```


## Installation

```bash
git clone https://github.com/dineshpinto/synchronous-gossip-protocol.git
cd synchronous-gossip-protocol
poetry install
poetry run python -m ipykernel install --user --name=synchronous-gossip-protocol
```

## Usage

```bash
poetry run jupyter lab
```
