"""Implementação de um jogo simples de Blackjack."""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from typing import Callable, Iterable, Iterator, Sequence

from .cards import Deck, Hand

DecisionSource = Callable[[Hand], str] | Iterable[str] | None


@dataclass
class RoundResult:
    """Resultado de uma rodada."""

    player_hand: Hand
    dealer_hand: Hand
    outcome: str
    explanation: str


class BlackjackGame:
    """Controla a lógica de uma partida de Blackjack."""

    def __init__(self, *, seed: int | None = None) -> None:
        self._rng = random.Random(seed)
        self._deck = Deck(rng=self._rng)

    def _fresh_hands(self) -> tuple[Hand, Hand]:
        if self._deck.remaining() < 15:
            self._deck.reset()
        player = Hand(self._deck.deal(2))
        dealer = Hand(self._deck.deal(2))
        return player, dealer

    def _dealer_turn(self, hand: Hand) -> None:
        while hand.value() < 17:
            hand.add(self._deck.draw())

    def _determine_winner(self, player: Hand, dealer: Hand) -> tuple[str, str]:
        if player.is_bust():
            return "dealer", "Você estourou 21. O dealer vence."
        if dealer.is_bust():
            return "player", "O dealer estourou 21. Você vence!"
        if player.value() > dealer.value():
            return "player", "Sua mão é maior. Você vence!"
        if player.value() < dealer.value():
            return "dealer", "O dealer tem mais pontos. Você perde."
        return "push", "Empate! Ambos têm o mesmo valor."

    def _decision_iterator(self, player: Hand, source: DecisionSource) -> Iterator[str]:
        if source is None:
            while True:
                yield "c" if player.value() < 17 else "p"
        elif callable(source):
            while True:
                yield source(player)
        else:
            iterator = iter(source)
            for decision in iterator:
                yield decision
            while True:
                yield "p"

    def play_round(self, decisions: DecisionSource = None) -> RoundResult:
        """Executa uma rodada de Blackjack.

        ``decisions`` pode ser ``None`` (estratégia automática simples), um
        iterável de decisões pré-determinadas ou uma função que recebe a mão do
        jogador e retorna "c" (comprar carta) ou "p" (parar).
        """

        player, dealer = self._fresh_hands()

        if player.is_blackjack() and dealer.is_blackjack():
            return RoundResult(player, dealer, "push", "Blackjack duplo! Empate.")
        if player.is_blackjack():
            return RoundResult(player, dealer, "player", "Blackjack natural! Você vence.")
        if dealer.is_blackjack():
            return RoundResult(player, dealer, "dealer", "O dealer tem Blackjack.")

        for decision in self._decision_iterator(player, decisions):
            if decision.lower().startswith("c"):
                player.add(self._deck.draw())
                if player.is_bust():
                    return RoundResult(player, dealer, "dealer", "Você estourou 21. O dealer vence.")
            elif decision.lower().startswith("p"):
                break

        self._dealer_turn(dealer)
        outcome, explanation = self._determine_winner(player, dealer)
        return RoundResult(player, dealer, outcome, explanation)

    def play_interactive(self) -> None:
        """Loop interativo para jogar via terminal."""

        print("Bem-vindo ao Blackjack!")
        keep_playing = True
        while keep_playing:
            result = self.play_round(self._interactive_decision)
            print("\nSuas cartas:", result.player_hand.formatted())
            print("Valor:", result.player_hand.value())
            print("Mão do dealer:", result.dealer_hand.formatted())
            print("Valor do dealer:", result.dealer_hand.value())
            print(result.explanation)
            again = input("Jogar novamente? (s/n): ").strip().lower()
            keep_playing = again == "s"
        print("Obrigado por jogar!")

    def _interactive_decision(self, hand: Hand) -> str:
        while True:
            choice = input("Digite 'c' para carta ou 'p' para parar: ").strip().lower()
            if choice in {"c", "p"}:
                return choice
            print("Opção inválida. Tente novamente.")


def run_demo(rounds: int, seed: int | None) -> None:
    game = BlackjackGame(seed=seed)
    for number in range(1, rounds + 1):
        result = game.play_round()
        print(f"Rodada {number}")
        print("Jogador:", result.player_hand.formatted(), f"({result.player_hand.value()} pontos)")
        print("Dealer:", result.dealer_hand.formatted(), f"({result.dealer_hand.value()} pontos)")
        print(result.explanation)
        print("-" * 40)


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Jogo de cartas Blackjack no terminal.")
    parser.add_argument("--demo", action="store_true", help="Executa rodadas automáticas de demonstração.")
    parser.add_argument("--rodadas", type=int, default=3, help="Quantidade de rodadas na demonstração.")
    parser.add_argument("--seed", type=int, default=None, help="Semente para o gerador aleatório.")
    args = parser.parse_args(argv)

    if args.demo:
        run_demo(args.rodadas, args.seed)
    else:
        game = BlackjackGame(seed=args.seed)
        game.play_interactive()


if __name__ == "__main__":  # pragma: no cover - entrada de módulo
    main()
