# Pac-Man com Minimax

Projeto de **Inteligência Artificial**, do curso de **Ciências da Computação**, com implementação de busca adversarial para controlar o Pac-Man.

**Membros:** Henrique Luza dos Santos e Eduardo Regueiro Costa.

**Professor:** Nikson Bernardes Fernandes Ferreira.

O Pac-Man escolhe a ação com o melhor resultado entre os piores cenários previstos. Ele é o agente **MAX**; cada fantasma é um agente **MIN**. A busca considera rodadas completas e termina ao alcançar a profundidade configurada, uma vitória, uma derrota ou um estado sem ações.

## Comece aqui

Na pasta do projeto, execute:

```bash
python3 pacman.py --pacman MinimaxAgent --depth 2 --layout smallClassic
```

Para uma demonstração com a heurística opcional:

```bash
python3 pacman.py -p MinimaxAgent --depth 2 -l smallClassic -a evalFn=better
```

Para executar sem janela, acrescente `-q`. Para acompanhar o tabuleiro no terminal, use `-t`:

```bash
python3 pacman.py -p MinimaxAgent --depth 2 -l smallClassic -a evalFn=better -q -f
python3 pacman.py -p MinimaxAgent --depth 1 -l minimaxClassic -t --frameTime 0.1
```

**Estudo detalhado:** [Guia de estudo do código](docs/ESTUDO_DO_CODIGO.md), com explicação de cada linha não vazia do arquivo de entrega, arquitetura, exemplos de recursão, testes e roteiro para apresentação.

## Requisitos e instalação

- Python 3.10 ou superior; validação realizada com Python **3.14.3**.
- Somente biblioteca padrão: não é necessário executar `pip install`.
- Tkinter com ambiente gráfico para abrir a janela. O modo `-q` funciona sem Tkinter.
- Execute os comandos de jogo a partir da raiz do repositório, onde está `pacman.py`.

Verifique o ambiente:

```bash
python3 --version
python3 -m tkinter
```

O segundo comando abre a janela de teste do Tkinter. Se o módulo não estiver disponível, use uma instalação de Python com suporte a Tk ou execute o jogo com `-q`/`-t`. No Windows, utilize `py -3` se `python3` não estiver registrado.

Um ambiente virtual é opcional:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No PowerShell, a ativação equivalente é `.venv\Scripts\Activate.ps1`.

## Comandos e parâmetros

| Parâmetro | Função | Exemplo |
| --- | --- | --- |
| `-p`, `--pacman` | Classe que controla o Pac-Man | `-p MinimaxAgent` |
| `--depth` | Rodadas completas previstas; inteiro positivo | `--depth 2` |
| `-a`, `--agentArgs` | Configuração do agente | `-a depth=2,evalFn=better` |
| `-l`, `--layout` | Mapa em `layouts/`, sem extensão | `-l smallClassic` |
| `-g`, `--ghosts` | Política dos fantasmas reais | `-g DirectionalGhost` |
| `-k`, `--numghosts` | Quantidade máxima de fantasmas do mapa | `-k 2` |
| `-n`, `--numGames` | Número de partidas | `-n 5` |
| `-f`, `--fixRandomSeed` | Fixa a semente aleatória do processo | `-f` |
| `-q` | Sem janela; imprime resultados | `-q` |
| `-t` | Tabuleiro no terminal | `-t` |
| `--frameTime` | Intervalo entre quadros | `--frameTime 0.1` |
| `-h`, `--help` | Ajuda completa da base | `-h` |

Sem configuração, `MinimaxAgent` usa profundidade **3** e `scoreEvaluationFunction`. O mapa padrão do motor é `mediumClassic`; para começar, prefira profundidades 1 ou 2 e mapas pequenos. O custo cresce exponencialmente.

A sintaxe original também funciona:

```bash
python3 pacman.py --pacman MinimaxAgent --agentArgs depth=2
```

A opção `--depth` foi adicionada ao motor para atender ao comando do enunciado. Se ela e `-a depth=...` forem usadas juntas, os valores devem coincidir. Profundidades zero e negativas são rejeitadas. `--depth` deve ser usado com um agente que aceite esse argumento.

### Outras demonstrações

```bash
# Mais rodadas de previsão em um mapa pequeno
python3 pacman.py -p MinimaxAgent --depth 3 -l minimaxClassic -q -f

# Fantasmas que tendem a perseguir o Pac-Man
python3 pacman.py -p MinimaxAgent --depth 2 -a evalFn=better -g DirectionalGhost -l smallClassic -q -f

# Jogar manualmente com setas ou WASD
python3 pacman.py -p KeyboardAgent -l smallClassic
```

## Organização

```text
Pacman-Minimax/
├── seuPacManAgents.py       # Entrega: Minimax e heurística opcional
├── pacman.py                # Estado, regras e inicialização do jogo
├── multiAgents.py           # Classe base e avaliação padrão fornecidas
├── game.py                  # Agentes, posições, grades e laço de turnos
├── ghostAgents.py           # Políticas dos fantasmas reais
├── layout.py                # Leitura de mapas
├── layouts/                 # Labirintos .lay da base
├── graphicsDisplay.py       # Desenho do jogo
├── graphicsUtils.py         # Operações Tkinter
├── textDisplay.py           # Saída textual ou silenciosa
├── keyboardAgents.py        # Controle humano
├── pacmanAgents.py          # Outros agentes fornecidos
├── util.py                  # Distâncias, coleções e funções auxiliares
├── autograder.py            # Corretor original
├── multiagentTestClasses.py # Testes de árvores e partidas da base
├── testClasses.py           # Infraestrutura das questões
├── testParser.py            # Leitura dos testes da base
├── grading.py               # Relatório de pontuação do corretor
├── projectParams.py         # Configuração original do corretor
├── test_cases/              # Questões e resultados esperados originais
├── scripts/
│   └── validar_minimax.py   # Executa somente q2 com seuPacManAgents
├── tests/
│   ├── test_minimax.py      # Árvores controladas e casos extremos
│   └── test_integracao.py   # GameState, heurística e CLI
├── docs/
│   └── ESTUDO_DO_CODIGO.md  # Material de estudo e apresentação
├── VERSION                  # Versão da base recebida
└── README.md
```

Os nomes públicos e a disposição do motor foram preservados porque seus imports, carregador de agentes e corretor dependem deles. A implementação nova está concentrada no arquivo exigido, e os materiais de apoio estão separados em pastas claras.

## Implementação

`MinimaxAgent` herda de `MultiAgentSearchAgent`. Dentro de `getAction`, a função aninhada `minimax` calcula valores; o laço da raiz guarda a ação associada ao maior valor.

1. Verifica vitória, derrota ou limite de profundidade e aplica `self.evaluationFunction`.
2. Obtém as ações legais; se não houver nenhuma, avalia o estado atual.
3. Calcula o próximo agente com `(agent_index + 1) % número_de_agentes`.
4. Incrementa a profundidade somente quando o próximo agente é o Pac-Man.
5. Gera sucessores e propaga o maior valor em MAX ou o menor valor em MIN.
6. Na raiz, retorna uma ação legal; empates preservam a primeira ação da lista.

`Stop` participa normalmente da busca. Em uma raiz terminal ou sem ações, o agente retorna `Directions.STOP` defensivamente. Não há poda alfa-beta, remoção de ações ou memorização que altere a expansão exigida pelo Minimax clássico.

### Avaliação padrão e heurística opcional

- **Padrão (`scoreEvaluationFunction`):** retorna a pontuação fornecida pelo motor; é a avaliação usada para verificar o algoritmo com q2.
- **Opcional (`better`):** considera pontuação, quantidade e proximidade de comida, cápsulas restantes, perigo de fantasmas ativos e oportunidade de alcançar fantasmas assustados. Vitória e derrota recebem infinito positivo e negativo.

A heurística opcional usa distâncias de Manhattan e pesos manuais. Ela não calcula caminhos contornando paredes, não aprende com partidas e não garante vitória. A implementação fornecida originalmente tinha sinais que desfavoreciam comida próxima e favoreciam fantasmas próximos; a versão usada por este agente corrige isso e aceita listas vazias.

Os fantasmas simulados pelo Minimax sempre minimizam. Os fantasmas **reais** obedecem a `RandomGhost` ou `DirectionalGhost`; portanto, podem agir de maneira diferente da hipótese pessimista da busca.

## Testes

Execute os dois comandos:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validar_minimax.py
```

- **24 testes adicionais:** decisões MAX/MIN, profundidade, múltiplos fantasmas, ausência de fantasmas, estados terminais, empates, ações vazias, imutabilidade do estado de entrada, heurística e argumentos.
- **34 testes originais de q2:** árvores com valores conhecidos, profundidades, estados terminais, expansão e uma partida integrada. Resultado observado: **5/5**.
- O arquivo de entrega também foi copiado isoladamente para uma cópia temporária da base original e executado com `-a depth=2,evalFn=better`, sem alterar o motor original. A partida terminou com vitória e pontuação 1654.
- O script adaptador retorna código de saída `0` quando q2 alcança 5/5 e `1` em caso de pontuação inferior.

O corretor original procura `MinimaxAgent` em `multiAgents`. O adaptador fornece `seuPacManAgents` sob essa chave, sem duplicar o algoritmo e sem alterar os testes ou resultados esperados. Use esse script: executar apenas `python3 autograder.py` tenta corrigir outras questões do curso, fora do escopo deste trabalho.

Validações complementares:

```bash
python3 -W error::SyntaxWarning -m compileall -q .
git diff --check
```

Strings de expressões regulares e arte ASCII do corretor receberam prefixo `r` para eliminar avisos de escapes nas versões recentes do Python.

### Resultados observados

Execuções em 05/10/2026, Python 3.14.3, profundidade 2, `-q -f`. Cada linha abaixo corresponde a um processo separado. A semente é fixada uma vez por processo, não reiniciada a cada partida.

| Mapa | Avaliação | Fantasma | Partidas | Vitórias | Média |
| --- | --- | --- | ---: | ---: | ---: |
| `minimaxClassic` | Padrão | `RandomGhost` | 3 | 2 | 178,33 |
| `smallClassic` | Padrão | `RandomGhost` | 5 | 1 | 24,60 |
| `smallClassic` | `better` | `RandomGhost` | 5 | 5 | 1518,60 |
| `smallClassic` | `better` | `DirectionalGhost` | 3 | 0 | -202,67 |

Para reproduzir a comparação de avaliação:

```bash
python3 pacman.py -p MinimaxAgent --depth 2 -l smallClassic -q -f -n 5
python3 pacman.py -p MinimaxAgent --depth 2 -l smallClassic -q -f -n 5 -a evalFn=better
```

São amostras pequenas, não uma garantia estatística. A nota do corretor verifica o algoritmo; uma derrota não implica implementação incorreta. O horizonte limitado e a qualidade da avaliação influenciam fortemente o resultado. A validação automatizada foi realizada em modo sem janela; a interface gráfica depende do Tkinter local.

## Entrega acadêmica

O arquivo solicitado pelo enunciado é **`seuPacManAgents.py`**, na raiz do projeto. Ele depende dos arquivos do jogo fornecidos pelo professor; não é um programa autônomo.

Para utilizá-lo na base original, copie somente esse arquivo para a pasta `pacman/` e use:

```bash
python3 pacman.py --pacman MinimaxAgent --agentArgs depth=2
```

Nesse caso, utilize `--agentArgs`: a opção de configuração `--depth` pertence à adaptação de `pacman.py` deste repositório. Os membros estão identificados no cabeçalho do arquivo de entrega.

## Dificuldades comuns

| Situação | Como resolver |
| --- | --- |
| `No module named tkinter` | Use `-q` ou uma instalação de Python com Tkinter. |
| Mapa não encontrado | Execute na raiz e confira o nome em `layouts/`. |
| Jogo demora a responder | Reduza para `--depth 1` ou `2` e use um mapa menor. |
| `--depth` não existe na pasta original | Use `-a depth=2` ou o motor deste repositório. |
| Corretor não encontra `MinimaxAgent` | Execute `python3 scripts/validar_minimax.py`. |
| Pac-Man fica parado ou perde | Compare `-a evalFn=better`, profundidades e mapas; a busca é limitada. |

## Histórico e créditos

Desenvolvimento na branch `codex/pacman-minimax`, em commits separados com mensagens Conventional Commits. A identidade Git utilizada é a configuração local do repositório, sem trailers de coautoria de agentes.

A base e seus testes são os **[Pacman AI Projects da UC Berkeley](http://ai.berkeley.edu)**. Os avisos originais de licença e atribuição foram preservados nos arquivos. O cabeçalho permite uso educacional condicionado à preservação dos créditos e à não publicação/distribuição de soluções. Este projeto mantém essas condições; não acrescenta uma licença permissiva sobre o material recebido.

O trabalho acrescenta o Minimax, a heurística opcional corrigida, a opção `--depth`, testes e documentação. Os arquivos de outras questões da base são mantidos como material original, sem alegação de que essas questões tenham sido implementadas.
