import random
from collections import Counter
from collections.abc import Generator
from enum import Enum


class Message(Enum):
    """ Enum class for message type """
    HONEST: int = 1
    ADVERSARIAL: int = 0


class NonSampleNode:
    """ Class for nodes not within the sample """

    def __init__(self):
        self.peers: list = []
        self.stored_messages: list[Message] = []
        self.counter: Counter = Counter()

    def broadcast(self) -> tuple[Message | None, list]:
        """ Broadcast the most common message """
        if self.counter:
            value = self.counter.most_common(1)[0][0]
            return value, self.peers
        return None, []

    def update(self, messages: list[Message]):
        """ Update the counter and storage """
        self.stored_messages.extend(messages)
        self.counter.update(messages)


class SampleNode:
    """ Class for nodes within the sample """

    def __init__(self, msg: Message):
        self.peers: list = []
        self.msg: Message = msg

    def broadcast(self) -> tuple[Message, list]:
        """ Broadcast the message to all peers """
        return self.msg, self.peers

    def update(self, _):
        pass


class NodePeerList:
    """ Class for the list of peers of a node """
    __slots__ = ('total_nodes', 'current_node')

    def __init__(
            self,
            total_nodes: list[SampleNode | NonSampleNode],
            current_node: SampleNode | NonSampleNode
    ):
        self.total_nodes = total_nodes
        self.current_node = current_node

    def __iter__(self) -> Generator:
        for node in self.total_nodes:
            if node != self.current_node:
                yield node


class NodeGenerator:
    """ Class for initializing nodes and generating connections """

    def __init__(
            self,
            num_non_sample_nodes: int,
            num_honest_sample_nodes: int,
            num_adversarial_sample_nodes: int,
            num_connected_nodes: int
    ):
        self.num_non_sample_nodes = num_non_sample_nodes
        self.num_honest_sample_nodes = num_honest_sample_nodes
        self.num_adversarial_sample_nodes = num_adversarial_sample_nodes
        self.num_connected_nodes = num_connected_nodes

    @staticmethod
    def _connect_all_nodes(
            total_nodes: list[SampleNode | NonSampleNode]
    ) -> Generator[SampleNode | NonSampleNode, list[SampleNode | NonSampleNode]]:
        """ Generate a fully connected graph """
        for current_node in total_nodes:
            yield current_node, NodePeerList(total_nodes, current_node)

    def randomly_connected_nodes(
            self,
            total_nodes: list,
    ) -> Generator[SampleNode | NonSampleNode, list[SampleNode | NonSampleNode]]:
        """ Generate a randomly connected graph """
        for node, peers in self._connect_all_nodes(total_nodes):
            yield node, random.sample([n for n in peers], self.num_connected_nodes)

    def initialize_nodes(self) -> tuple[list[SampleNode], list[NonSampleNode]]:
        """ Initialize the nodes """
        # Init adversarial sample nodes to Message.ADVERSARIAL
        sample_nodes = [
            SampleNode(Message.ADVERSARIAL) for _ in range(self.num_adversarial_sample_nodes)
        ]
        # Init honest sample nodes to Message.HONEST
        sample_nodes.extend(
            SampleNode(Message.HONEST) for _ in range(self.num_honest_sample_nodes)
        )
        non_sample_nodes = [NonSampleNode() for _ in range(self.num_non_sample_nodes)]
        return sample_nodes, non_sample_nodes

    @staticmethod
    def link_nodes_to_peers(generator: Generator):
        """ Link the nodes to peers """
        for node, peers in generator:
            node.peers = peers
