# Jogo de Cartas - Blackjack

Este projeto contém um jogo de cartas estilo Blackjack jogável diretamente no
terminal. O jogo está disponível em português e oferece dois modos:

- **Interativo**: você toma decisões digitando `c` (comprar carta) ou `p`
  (parar).
- **Demonstração**: o computador joga automaticamente utilizando uma estratégia
  simples (comprar até atingir 17 pontos).

## Pré-requisitos

- Python 3.10 ou superior.

## Como jogar

Execute no terminal, a partir da raiz do repositório:

```bash
python -m card_game
```

Você poderá jogar quantas rodadas quiser. Para sair, responda `n` quando
perguntado se deseja jogar novamente.

## Modo demonstração

Para assistir rodadas automáticas, execute:

```bash
python -m card_game --demo --rodadas 5 --seed 42
```

- `--rodadas` define quantas rodadas serão jogadas.
- `--seed` opcionalmente fixa a semente do gerador aleatório para tornar o
  resultado reproduzível.
