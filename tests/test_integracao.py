"""Verifica o agente com o GameState real e os argumentos do terminal."""

from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
import unittest

from layout import Layout
from pacman import GameState, readCommand
from seuPacManAgents import MinimaxAgent, betterEvaluationFunction


def make_state(rows=None, ghosts=2):
    """Cria um mapa pequeno, sem janela e sem depender de arquivos externos."""
    if rows is None:
        rows = ["%%%%%%%%%", "%P .   G%", "%   o G %", "%%%%%%%%%"]
    state = GameState()
    state.initialize(Layout(rows), ghosts)
    return state


class IntegrationTests(unittest.TestCase):
    def test_real_state_is_preserved_and_action_is_legal(self):
        state = make_state()
        original = state.deepCopy()
        action = MinimaxAgent(depth=2).getAction(state)
        self.assertIn(action, state.getLegalActions(0))
        self.assertEqual(state, original)

    def test_better_alias_uses_the_delivery_file_function(self):
        for name in ("better", "betterEvaluationFunction"):
            self.assertIs(MinimaxAgent(evalFn=name).evaluationFunction, betterEvaluationFunction)

    def test_qualified_evaluation_name_remains_supported(self):
        agent = MinimaxAgent(evalFn="seuPacManAgents.betterEvaluationFunction")
        self.assertIs(agent.evaluationFunction, betterEvaluationFunction)

    def test_food_proximity_increases_value(self):
        near = make_state(["%%%%%%%%%", "%P.     %", "%%%%%%%%%"], ghosts=0)
        far = make_state(["%%%%%%%%%", "%P    . %", "%%%%%%%%%"], ghosts=0)
        self.assertGreater(betterEvaluationFunction(near), betterEvaluationFunction(far))

    def test_dangerous_ghost_proximity_decreases_value(self):
        near = make_state(["%%%%%%%%%", "%PG   . %", "%%%%%%%%%"], ghosts=1)
        far = make_state(["%%%%%%%%%", "%P   G. %", "%%%%%%%%%"], ghosts=1)
        self.assertLess(betterEvaluationFunction(near), betterEvaluationFunction(far))

    def test_scared_ghost_can_be_attractive(self):
        dangerous = make_state()
        scared = dangerous.deepCopy()
        for ghost in scared.getGhostStates():
            ghost.scaredTimer = 20
        self.assertGreater(betterEvaluationFunction(scared), betterEvaluationFunction(dangerous))

    def test_empty_food_and_ghost_lists_are_supported(self):
        state = make_state(["%%%%%", "% P %", "%%%%%"], ghosts=0)
        self.assertEqual(betterEvaluationFunction(state), 0)

    def test_terminal_heuristic_values(self):
        for flag, expected in (("_win", float("inf")), ("_lose", -float("inf"))):
            state = make_state()
            setattr(state.data, flag, True)
            self.assertEqual(betterEvaluationFunction(state), expected)

    def command(self, *args):
        layout_path = Path(__file__).resolve().parents[1] / "layouts/minimaxClassic.lay"
        return readCommand(["-p", "MinimaxAgent", "-q", "-l", str(layout_path), *args])

    def test_depth_option_and_agent_arguments(self):
        args = self.command("--depth", "2", "-a", "evalFn=better")
        self.assertIsInstance(args["pacman"], MinimaxAgent)
        self.assertEqual(args["pacman"].depth, 2)
        self.assertIs(args["pacman"].evaluationFunction, betterEvaluationFunction)

    def test_original_agent_depth_syntax_is_supported(self):
        self.assertEqual(self.command("-a", "depth=1")["pacman"].depth, 1)

    def test_conflicting_or_invalid_depth_options_fail(self):
        cases = [("--depth", "0"), ("--depth", "-1"), ("--depth", "abc"),
                 ("--depth", "2", "-a", "depth=1")]
        for arguments in cases:
            with self.subTest(arguments=arguments), redirect_stderr(StringIO()):
                with self.assertRaises(SystemExit) as error:
                    self.command(*arguments)
                self.assertEqual(error.exception.code, 2)

    def test_repeated_consistent_depth_is_supported(self):
        self.assertEqual(self.command("--depth", "2", "-a", "depth=2")["pacman"].depth, 2)


if __name__ == "__main__":
    unittest.main()
