from unittest import TestCase

import synchronous_gossip_protocol as sgp


class NodeGenerationTest(TestCase):
    def setUp(self) -> None:
        self.num_non_sample_nodes = 100
        self.num_honest_sample_nodes = 20
        self.num_adversarial_sample_nodes = 10
        self.num_connected_nodes = 10
        self.time_steps = 25

    def test_run(self):
        states = sgp.generate_nodes_and_run_stf(
            num_non_sample_nodes=self.num_non_sample_nodes,
            num_honest_sample_nodes=self.num_honest_sample_nodes,
            num_adversarial_sample_nodes=self.num_adversarial_sample_nodes,
            num_connected_nodes=self.num_connected_nodes,
            time_steps=self.time_steps
        )
        self.assertEqual(len(states), self.time_steps)
