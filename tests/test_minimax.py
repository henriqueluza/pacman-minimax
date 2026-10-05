"""Testes determinísticos de decisões, profundidade e casos extremos."""

import unittest

from game import Directions
from seuPacManAgents import MinimaxAgent


class TreeState:
    """Estado mínimo: arestas têm agente/ação; consultas indevidas falham."""

    def __init__(self, tree, node="root", agents=2, visited=None):
        self.tree = tree
        self.node = node
        self.agents = agents
        self.visited = [] if visited is None else visited

    def isWin(self):
        return self.tree[self.node].get("win", False)

    def isLose(self):
        return self.tree[self.node].get("lose", False)

    def getScore(self):
        return self.tree[self.node].get("score", 0)

    def getNumAgents(self):
        return self.agents

    def getLegalActions(self, agent_index):
        data = self.tree[self.node]
        if self.isWin() or self.isLose():
            raise AssertionError("Estado terminal não deve ser expandido")
        if "agent" in data:
            assert agent_index == data["agent"], "Ordem incorreta de agentes"
        return list(data.get("edges", {}))

    def generateSuccessor(self, agent_index, action):
        self.visited.append((self.node, agent_index, action))
        node = self.tree[self.node]["edges"][action]
        return TreeState(self.tree, node, self.agents, self.visited)


class MinimaxTests(unittest.TestCase):
    def test_maximizes_the_worst_case_instead_of_the_best_leaf(self):
        state = TreeState({
            "root": {"agent": 0, "edges": {"risco": "a", "seguro": "b"}},
            "a": {"agent": 1, "edges": {"x": "a1", "y": "a2"}},
            "b": {"agent": 1, "edges": {"x": "b1", "y": "b2"}},
            "a1": {"score": 100}, "a2": {"score": -10},
            "b1": {"score": 3}, "b2": {"score": 5},
        })
        self.assertEqual(MinimaxAgent(depth=1).getAction(state), "seguro")
        self.assertEqual(len(state.visited), 6)
        self.assertEqual(state.node, "root")

    def test_both_ghosts_move_before_depth_cutoff(self):
        state = TreeState({
            "root": {"agent": 0, "edges": {"a": "a", "b": "b"}},
            "a": {"agent": 1, "score": 100, "edges": {"x": "a2"}},
            "b": {"agent": 1, "score": -100, "edges": {"x": "b2"}},
            "a2": {"agent": 2, "score": 100, "edges": {"x": "a3"}},
            "b2": {"agent": 2, "score": -100, "edges": {"x": "b3"}},
            "a3": {"score": -5}, "b3": {"score": 4},
        }, agents=3)
        self.assertEqual(MinimaxAgent(depth=1).getAction(state), "b")
        self.assertEqual([agent for _, agent, _ in state.visited], [0, 1, 2, 0, 1, 2])

    def test_second_round_changes_the_decision(self):
        tree = {
            "root": {"agent": 0, "edges": {"a": "a", "b": "b"}},
            "a": {"agent": 1, "edges": {"x": "a2"}},
            "b": {"agent": 1, "edges": {"x": "b2"}},
            "a2": {"agent": 0, "score": 10, "edges": {"x": "a3", "y": "a4"}},
            "b2": {"agent": 0, "score": 5, "edges": {"x": "b3"}},
            "a3": {"agent": 1, "edges": {"x": "end_a"}},
            "a4": {"agent": 1, "edges": {"x": "end_a4"}},
            "b3": {"agent": 1, "edges": {"x": "end_b"}},
            "end_a": {"score": -20}, "end_a4": {"score": -10},
            "end_b": {"score": 1},
        }
        self.assertEqual(MinimaxAgent(depth=1).getAction(TreeState(tree)), "a")
        self.assertEqual(MinimaxAgent(depth=2).getAction(TreeState(tree)), "b")

    def test_terminal_successors_are_evaluated_without_expansion(self):
        state = TreeState({
            "root": {"edges": {"perder": "loss", "ganhar": "win"}},
            "loss": {"lose": True, "score": -500},
            "win": {"win": True, "score": 500},
        })
        self.assertEqual(MinimaxAgent(depth=3).getAction(state), "ganhar")
        self.assertEqual(len(state.visited), 2)

    def test_terminal_root_returns_stop(self):
        for terminal in ("win", "lose"):
            with self.subTest(terminal=terminal):
                state = TreeState({"root": {terminal: True}})
                self.assertEqual(MinimaxAgent().getAction(state), Directions.STOP)
                self.assertEqual(state.visited, [])

    def test_root_without_actions_returns_stop(self):
        self.assertEqual(MinimaxAgent().getAction(TreeState({"root": {}})), Directions.STOP)

    def test_ghost_without_actions_uses_evaluation(self):
        state = TreeState({
            "root": {"edges": {"a": "a", "b": "b"}},
            "a": {"score": -4}, "b": {"score": 7},
        })
        self.assertEqual(MinimaxAgent().getAction(state), "b")

    def test_first_legal_action_wins_ties_even_at_negative_infinity(self):
        for score in (3, -float("inf")):
            with self.subTest(score=score):
                state = TreeState({
                    "root": {"edges": {"primeira": "a", "segunda": "b"}},
                    "a": {"score": score}, "b": {"score": score},
                })
                self.assertEqual(MinimaxAgent(depth=1).getAction(state), "primeira")

    def test_stop_is_considered_when_it_is_the_best_move(self):
        state = TreeState({
            "root": {"edges": {"andar": "a", Directions.STOP: "b"}},
            "a": {"score": -1}, "b": {"score": 1},
        })
        self.assertEqual(MinimaxAgent(depth=1).getAction(state), Directions.STOP)

    def test_no_ghosts_still_advances_depth(self):
        state = TreeState({
            "root": {"agent": 0, "edges": {"a": "a", "b": "b"}},
            "a": {"score": 2, "edges": {"extra": "missing"}},
            "b": {"score": 4, "edges": {"extra": "missing"}},
        }, agents=1)
        self.assertEqual(MinimaxAgent(depth=1).getAction(state), "b")
        self.assertEqual(len(state.visited), 2)

    def test_configured_evaluation_is_used(self):
        state = TreeState({
            "root": {"edges": {"a": "a", "b": "b"}},
            "a": {"score": 2}, "b": {"score": 4},
        })
        agent = MinimaxAgent(depth=1)
        agent.evaluationFunction = lambda leaf: -leaf.getScore()
        self.assertEqual(agent.getAction(state), "a")

    def test_invalid_depth_is_rejected(self):
        for depth in (0, -1, "abc", "1.5"):
            with self.subTest(depth=depth):
                with self.assertRaises(ValueError):
                    MinimaxAgent(depth=depth)


if __name__ == "__main__":
    unittest.main()
