![unittest](https://github.com/dineshpinto/synchronous-gossip-protocol/actions/workflows/unittest.yml/badge.svg)
[![codecov](https://codecov.io/gh/dineshpinto/synchronous-gossip-protocol/graph/badge.svg?token=H98PQDY5OE)](https://codecov.io/gh/dineshpinto/synchronous-gossip-protocol)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)

# synchronous-gossip-protocol

Python implementation of a synchronous gossip protocol. 

For a (blazingly fast) implementation in Rust see [dineshpinto/gossip-protocol-rs](https://github.com/dineshpinto/gossip-protocol-rs)

## Schema

```mermaid
flowchart TD
    GossipProtocolParams --> NodeGenerator;
    NodeGenerator -- list --> NonSampleNode;
    NodeGenerator -- list --> Adversarial;
    NodeGenerator -- list --> Honest;
    Adversarial --> Nodes;
    Honest --> Nodes;
    NonSampleNode --> Nodes;
    Nodes --> NetworkState;
    subgraph NetworkState
        NodeState --> StateTransitionFunction
        StateTransitionFunction --> NodeState;
        NodeState --o Counter;
        NodeState --o Storage;
    end
```

- Protocol library code is located in `synchronous_gossip_protocol/`
- Theory and simulation code are in a JupyterLab Notebook `synchronous_gossip.ipynb`
- Unittest cases are in `tests/`


## Installation

```bash
git clone https://github.com/dineshpinto/synchronous-gossip-protocol.git
cd synchronous-gossip-protocol
poetry install --with dev
poetry run python -m ipykernel install --user --name=synchronous-gossip-protocol
```

## Usage

```bash
poetry run jupyter lab
```

Open `synchronous_gossip.ipynb` and run all cells.
