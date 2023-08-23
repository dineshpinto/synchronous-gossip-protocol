from .node import NodeGenerator, NodePeerList, Message
from .state_transition import StateTransitionFunction

__all__ = ["NodeGenerator", "StateTransitionFunction", "NodePeerList", "Message"]


def generate_nodes_and_run_stf(
        num_non_sample_nodes: int,
        num_honest_sample_nodes: int,
        num_adversarial_sample_nodes: int,
        num_connected_nodes: int,
        time_steps: int
):
    node_generator = NodeGenerator(
        num_non_sample_nodes=num_non_sample_nodes,
        num_honest_sample_nodes=num_honest_sample_nodes,
        num_adversarial_sample_nodes=num_adversarial_sample_nodes,
        num_connected_nodes=num_connected_nodes
    )

    sample_nodes, non_sample_nodes = node_generator.initialize_nodes()

    node_generator.link_nodes(
        generator=node_generator.randomly_connected_nodes(
            total_nodes=sample_nodes + non_sample_nodes,
        )
    )

    state_transition_func = StateTransitionFunction(
        sample_nodes=sample_nodes,
        non_sample_nodes=non_sample_nodes,
        node_generator=node_generator
    )

    states = state_transition_func.iterate_state(time_steps)
    return states
