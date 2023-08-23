from unittest import TestCase

import synchronous_gossip_protocol as sgp


class StateTransitionTest(TestCase):
    def setUp(self) -> None:
        self.num_non_sample_nodes = 100
        self.num_honest_sample_nodes = 20
        self.num_adversarial_sample_nodes = 10
        self.num_connected_nodes = 10
        self.time_steps = 25

    def test_state_transition_setup(self):
        self.node_generator = sgp.NodeGenerator(
            num_non_sample_nodes=self.num_non_sample_nodes,
            num_honest_sample_nodes=self.num_honest_sample_nodes,
            num_adversarial_sample_nodes=self.num_adversarial_sample_nodes,
            num_connected_nodes=self.num_connected_nodes
        )

    def test_state_iteration(self):
        self.node_generator = sgp.NodeGenerator(
            num_non_sample_nodes=self.num_non_sample_nodes,
            num_honest_sample_nodes=self.num_honest_sample_nodes,
            num_adversarial_sample_nodes=self.num_adversarial_sample_nodes,
            num_connected_nodes=self.num_connected_nodes
        )

        self.sample_nodes, self.non_sample_nodes = self.node_generator.initialize_nodes()
        self.node_generator.link_nodes(
            generator=self.node_generator.randomly_connected_nodes(
                total_nodes=self.sample_nodes + self.non_sample_nodes,
            )
        )

        state_transition_func = sgp.StateTransitionFunction(
            sample_nodes=self.sample_nodes,
            non_sample_nodes=self.non_sample_nodes,
            node_generator=self.node_generator
        )

        states = state_transition_func.iterate_state(self.time_steps)
        self.assertEqual(len(states), self.time_steps)
