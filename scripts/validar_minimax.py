"""Executa a questão q2 original usando o agente no arquivo de entrega."""

from pathlib import Path
import os
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import autograder
import multiagentTestClasses
import seuPacManAgents
import textDisplay


def main():
    """Adapta o nome esperado pelo corretor sem duplicar a implementação."""
    os.chdir(PROJECT_ROOT)
    modules = {
        "multiAgents": seuPacManAgents,
        "projectTestClasses": multiagentTestClasses,
    }
    points = autograder.evaluate(
        generateSolutions=False,
        testRoot="test_cases",
        moduleDict=modules,
        questionToGrade="q2",
        display=textDisplay.NullGraphics(),
    )
    return 0 if points["q2"] == 5 else 1


if __name__ == "__main__":
    sys.exit(main())
