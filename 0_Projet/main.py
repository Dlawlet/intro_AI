### Attention, si tu veux conserver ce qui est mis dans le terminal, lance "python3 tester.py" ###

from gameClass import Game
if __name__ == "__main__":
    game = Game()
    first_player = "Human"
    second_player = "Minimax"
    winner = game.run(first=first_player, second=second_player)
    print(f"#{first_player}# VS #{second_player}#. The winner is : #{winner}#")
