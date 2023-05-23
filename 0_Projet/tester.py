import subprocess

"""
    Pour la personne qui lit ce code:
        tester.py permet de lancer le programme main.py et de récupérer ce qui est écrit dans le terminal.
        Il faut savoir que main.py écrit LUI-MEME dans files/win_rate.txt le résultat de la partie.
"""

def run_test():      
    # Run a command in the terminal
    cmd = "python3 main.py"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

    # Capture the output and write it to a file
    with open("files/terminal.txt", "w") as f:
        f.write(result.stdout.decode("utf-8", errors="ignore"))
    
    print("done")

run_nbr = 1
for _ in range(run_nbr):
    run_test()