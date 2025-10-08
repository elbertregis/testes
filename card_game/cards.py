"""Componentes básicos de cartas utilizados no jogo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List
import random

SUITS = ["Copas", "Ouros", "Paus", "Espadas"]
RANKS = [
    ("A", 1),
    ("2", 2),
    ("3", 3),
    ("4", 4),
    ("5", 5),
    ("6", 6),
    ("7", 7),
    ("8", 8),
    ("9", 9),
    ("10", 10),
    ("J", 10),
    ("Q", 10),
    ("K", 10),
]


@dataclass(frozen=True)
class Card:
    """Representa uma carta de baralho."""

    rank: str
    suit: str

    @property
    def value(self) -> int:
        """Valor base da carta considerando regras do Blackjack."""

        for r, value in RANKS:
            if r == self.rank:
                return value
        raise ValueError(f"Rank desconhecido: {self.rank}")

    def __str__(self) -> str:  # pragma: no cover - método trivial
        return f"{self.rank} de {self.suit}"


class Deck:
    """Baralho padrão com 52 cartas."""

    def __init__(self, *, rng: random.Random | None = None) -> None:
        self._rng = rng or random.Random()
        self._cards: List[Card] = []
        self.reset()

    def reset(self) -> None:
        """Recria um baralho completo e o embaralha."""

        self._cards = [Card(rank, suit) for suit in SUITS for rank, _ in RANKS]
        self.shuffle()

    def shuffle(self) -> None:
        """Embaralha o baralho."""

        self._rng.shuffle(self._cards)

    def draw(self) -> Card:
        """Retira uma carta do topo do baralho."""

        if not self._cards:
            raise RuntimeError("O baralho acabou. Reinicie a partida.")
        return self._cards.pop()

    def remaining(self) -> int:
        """Quantidade de cartas restantes."""

        return len(self._cards)

    def deal(self, quantity: int) -> List[Card]:
        """Retorna múltiplas cartas de uma só vez."""

        if quantity < 0:
            raise ValueError("A quantidade deve ser positiva.")
        return [self.draw() for _ in range(quantity)]


class Hand:
    """Representa uma mão de Blackjack."""

    def __init__(self, cards: Iterable[Card] | None = None) -> None:
        self.cards: List[Card] = list(cards or [])

    def add(self, card: Card) -> None:
        self.cards.append(card)

    def value(self) -> int:
        """Calcula o melhor valor possível para a mão."""

        total = sum(card.value for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == "A")
        while aces > 0 and total + 10 <= 21:
            total += 10
            aces -= 1
        return total

    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.value() == 21

    def is_bust(self) -> bool:
        return self.value() > 21

    def formatted(self, hide_first: bool = False) -> str:
        """Representação textual da mão."""

        if hide_first and self.cards:
            hidden = ["[CARTA VIRADA]"] + [str(card) for card in self.cards[1:]]
            return ", ".join(hidden)
        return ", ".join(str(card) for card in self.cards)
