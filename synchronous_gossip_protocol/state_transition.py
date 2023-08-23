from collections import Counter, defaultdict

from .node import Message, NonSampleNode, SampleNode


class StateTransitionFunction:
    """ Class for the state transition function """

    def __init__(
            self,
            sample_nodes: list[SampleNode],
            non_sample_nodes: list[NonSampleNode]
    ):
        self.sample_nodes = sample_nodes
        self.non_sample_nodes = non_sample_nodes

    @staticmethod
    def broadcast(
            node: SampleNode | NonSampleNode,
            message_queue: defaultdict
    ) -> Message | None:
        """ Broadcast the message from a node to its peers """
        message, peers = node.broadcast()
        if message is not None:
            for p in peers:
                message_queue[p][message] += 1
            return message
        return None

    @staticmethod
    def update_all_nodes(message_queue: defaultdict):
        """ Update the internal state of all nodes """
        for node, messages in message_queue.items():
            node.update(messages)

    def iterate_state(self, time_steps: int) -> list[list[int]]:
        """ Iterate the state of the network in time """
        message_queue = defaultdict(Counter)

        messages = []

        for idx in range(1, time_steps + 1):
            assert not message_queue

            _messages_non_sample = []
            for node in self.non_sample_nodes:
                msg = self.broadcast(node, message_queue)
                _messages_non_sample.append(msg.value if msg is not None else None)

            _messages_sample = []
            for node in self.sample_nodes:
                msg = self.broadcast(node, message_queue)
                _messages_sample.append(msg.value if msg is not None else None)

            messages.append(_messages_non_sample + _messages_sample)

            self.update_all_nodes(message_queue)
            message_queue.clear()

        return messages
