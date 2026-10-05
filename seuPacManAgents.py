# seuPacManAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""Agente Minimax do trabalho de Inteligência Artificial.

Membros: Henrique Luza dos Santos e Eduardo Regueiro Costa.
"""

from game import Directions
from multiAgents import MultiAgentSearchAgent
from pacman import GameState
from util import manhattanDistance


class MinimaxAgent(MultiAgentSearchAgent):
    """Busca adversarial: Pac-Man maximiza e todos os fantasmas minimizam."""

    def __init__(self, evalFn="scoreEvaluationFunction", depth="3"):
        # A classe base configura o índice 0, a avaliação e a profundidade.
        super().__init__(depth=depth)
        if self.depth < 1:
            raise ValueError("A profundidade deve ser um inteiro maior ou igual a 1.")
        if evalFn in ("better", "betterEvaluationFunction"):
            self.evaluationFunction = betterEvaluationFunction
        elif evalFn != "scoreEvaluationFunction":
            # Mantém compatibilidade com funções qualificadas por módulo.
            super().__init__(evalFn=evalFn, depth=depth)

    def getAction(self, gameState: GameState):
        """Retorna a melhor ação após simular self.depth rodadas completas."""

        def minimax(state, agent_index, depth):
            # Folhas retornam valores; nunca tentamos expandir estados terminais.
            if state.isWin() or state.isLose() or depth >= self.depth:
                return self.evaluationFunction(state)

            legal_actions = state.getLegalActions(agent_index)
            if not legal_actions:
                return self.evaluationFunction(state)

            next_agent = (agent_index + 1) % state.getNumAgents()
            next_depth = depth + (1 if next_agent == self.index else 0)

            if agent_index == self.index:
                best_value = -float("inf")
                for action in legal_actions:
                    successor = state.generateSuccessor(agent_index, action)
                    value = minimax(successor, next_agent, next_depth)
                    best_value = max(best_value, value)
                return best_value

            best_value = float("inf")
            for action in legal_actions:
                successor = state.generateSuccessor(agent_index, action)
                value = minimax(successor, next_agent, next_depth)
                best_value = min(best_value, value)
            return best_value

        # A raiz escolhe uma ação; a função recursiva sempre retorna um número.
        if gameState.isWin() or gameState.isLose():
            return Directions.STOP
        legal_actions = gameState.getLegalActions(self.index)
        if not legal_actions:
            return Directions.STOP

        best_action = legal_actions[0]
        best_value = -float("inf")
        next_agent = (self.index + 1) % gameState.getNumAgents()
        next_depth = 1 if next_agent == self.index else 0
        for action in legal_actions:
            successor = gameState.generateSuccessor(self.index, action)
            value = minimax(successor, next_agent, next_depth)
            # O primeiro movimento legal vence empates, inclusive com -infinito.
            if value > best_value:
                best_value = value
                best_action = action
        return best_action


def betterEvaluationFunction(currentGameState: GameState):
    """Heurística opcional: pontuação, comida, cápsulas e risco de colisão."""
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return -float("inf")

    position = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    value = currentGameState.getScore() - 4 * len(food) - 3 * len(capsules)

    if food:
        nearest_food = min(manhattanDistance(position, dot) for dot in food)
        value += 10 / (nearest_food + 1)

    for ghost in currentGameState.getGhostStates():
        distance = manhattanDistance(position, ghost.getPosition())
        if ghost.scaredTimer > distance:
            # Um fantasma só atrai se a distância estimada couber no temporizador.
            value += 20 / (distance + 1)
        elif ghost.scaredTimer == 0:
            value -= 12 / (distance + 1)
            if distance <= 1:
                value -= 200

    return value


# Nome curto aceito em --agentArgs evalFn=better.
better = betterEvaluationFunction
