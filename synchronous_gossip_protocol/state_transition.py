from collections import Counter, defaultdict

from tqdm import tqdm

from .node import Message, NonSampleNode, SampleNode, NodeGenerator


class StateTransitionFunction:
    """ Class for the state transition function """

    def __init__(
            self,
            sample_nodes: list[SampleNode],
            non_sample_nodes: list[NonSampleNode],
            node_generator: NodeGenerator,
    ):
        self.sample_nodes = sample_nodes
        self.non_sample_nodes = non_sample_nodes
        self.node_generator = node_generator

    @staticmethod
    def _add_messages_to_queue(
            node: SampleNode | NonSampleNode,
            message_queue: defaultdict
    ) -> Message | None:
        """ Broadcast the message from a node to its peers """
        message, peers = node.broadcast()
        if message is not None:
            for peer in peers:
                message_queue[peer][message] += 1
            return message
        return None

    @staticmethod
    def _update_all_nodes(message_queue: defaultdict):
        """ Update the internal state of all nodes """
        for node, messages in message_queue.items():
            node.update(messages)

    def iterate_state(
            self,
            time_steps: int,
            resample_peers_each_step: bool = False,
            progress_bar: bool = False
    ) -> list[list[int]]:
        """ Iterate the state of the network in time """
        message_queue = defaultdict(Counter)

        messages = []

        for _ in tqdm(range(1, time_steps + 1), disable=not progress_bar):
            assert not message_queue

            _messages_non_sample = []
            for node in self.non_sample_nodes:
                msg = self._add_messages_to_queue(node, message_queue)
                _messages_non_sample.append(msg.value if msg is not None else None)

            _messages_sample = []
            for node in self.sample_nodes:
                msg = self._add_messages_to_queue(node, message_queue)
                _messages_sample.append(msg.value if msg is not None else None)

            messages.append(_messages_non_sample + _messages_sample)

            self._update_all_nodes(message_queue)
            message_queue.clear()

            if resample_peers_each_step:
                self.node_generator.link_nodes_to_peers(
                    generator=self.node_generator.randomly_connected_nodes(
                        total_nodes=self.sample_nodes + self.non_sample_nodes,
                    )
                )

        return messages
