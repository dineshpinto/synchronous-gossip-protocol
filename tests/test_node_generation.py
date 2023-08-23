from unittest import TestCase

import synchronous_gossip_protocol as sgp


class NodeGenerationTest(TestCase):
    def setUp(self) -> None:
        self.num_non_sample_nodes = 100
        self.num_honest_sample_nodes = 20
        self.num_adversarial_sample_nodes = 10
        self.num_connected_nodes = 10

    def test_node_generator_setup(self):
        self.node_generator = sgp.NodeGenerator(
            num_non_sample_nodes=self.num_non_sample_nodes,
            num_honest_sample_nodes=self.num_honest_sample_nodes,
            num_adversarial_sample_nodes=self.num_adversarial_sample_nodes,
            num_connected_nodes=self.num_connected_nodes
        )

    def test_node_initialization(self):
        self.node_generator = sgp.NodeGenerator(
            num_non_sample_nodes=self.num_non_sample_nodes,
            num_honest_sample_nodes=self.num_honest_sample_nodes,
            num_adversarial_sample_nodes=self.num_adversarial_sample_nodes,
            num_connected_nodes=self.num_connected_nodes
        )

        self.sample_nodes, self.non_sample_nodes = self.node_generator.initialize_nodes()
        self.assertEqual(
            len(self.sample_nodes),
            self.num_honest_sample_nodes + self.num_adversarial_sample_nodes
        )
        self.assertEqual(len(self.non_sample_nodes), self.num_non_sample_nodes)

    def test_node_linking(self):
        self.node_generator = sgp.NodeGenerator(
            num_non_sample_nodes=self.num_non_sample_nodes,
            num_honest_sample_nodes=self.num_honest_sample_nodes,
            num_adversarial_sample_nodes=self.num_adversarial_sample_nodes,
            num_connected_nodes=self.num_connected_nodes
        )

        self.sample_nodes, self.non_sample_nodes = self.node_generator.initialize_nodes()

        self.node_generator.link_nodes_to_peers(
            generator=self.node_generator.randomly_connected_nodes(
                total_nodes=self.sample_nodes + self.non_sample_nodes,
            )
        )
        self.assertIsInstance(self.sample_nodes[0].peers, list)
