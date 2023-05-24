### Attention, si tu veux conserver ce qui est mis dans le terminal, lance "python3 tester.py" ###
import sys
from gameClass import Game
if __name__ == "__main__":
    game = Game()

    script_name = sys.argv[0]
    script_arguments = sys.argv[1:]

    first_player = script_arguments[0]
    second_player = script_arguments[1]

    winner = game.run(first=first_player, second=second_player)

    with open("files/stat.txt", "a") as f:
        f.write(f"#{first_player}# VS #{second_player}#. The winner is : #{winner}#\n")