### Attention, si tu veux conserver ce qui est mis dans le terminal, lance "python3 tester.py" ###

from gameClass import Game
if __name__ == "__main__":
    game = Game()
    winner = game.run(first="Random_IA", second="Random_IA")
    print("The winner is : ", winner)
