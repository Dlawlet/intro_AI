import subprocess
import sys
from time import sleep

"""
Pour la personne qui lit ce code:
    tester.py permet de lancer le programme main.py et de récupérer ce qui est écrit dans le terminal.
    Il faut savoir que main.py écrit LUI-MEME dans files/win_rate.txt le résultat de la partie.
"""

def pick_terminal_arguments():
    #script_name = sys.argv[0]
    script_arguments = sys.argv[1:]
    
    if len(script_arguments)!=0:
        first_player = script_arguments[0]
        second_player = script_arguments[1]
        run_nbr_terminal = int(script_arguments[2])
    else:
        first_player = "Human"
        second_player = "Minimax"
        run_nbr_terminal = 1
    return first_player,second_player,run_nbr_terminal

def run_test(first_player,second_player):      
    # Run a command in the terminal
    cmd = f"python3 main.py "+first_player+" "+second_player
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

    # Capture the output and write it to a file
    with open("files/terminal.txt", "w") as f:
        f.write(result.stdout.decode("utf-8", errors="ignore"))
    
    print("done")

def run_stat_calculator(to_write=True):
    # Run a command in the terminal
    cmd = "python3 stat_calculator.py"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

    if to_write:
        # Capture the output and write it to a file
        with open("files/terminal.txt", "w") as f:
            f.write(result.stdout.decode("utf-8", errors="ignore"))

    print("run_stat_calculator done")


def testing():
    first_player,second_player,run_nbr_terminal = pick_terminal_arguments()
    run_nbr = run_nbr_terminal

    for _ in range(run_nbr):
        run_test(first_player,second_player)

if __name__ == "__main__":
    # Clear the stat.txt file
    with open("files/stat.txt", "w") as f:
            f.write("")
    
    testing()
    sleep(1)
    run_stat_calculator()