import subprocess

# Run a command in the terminal
cmd = "python3 main.py"
result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

# Capture the output and write it to a file
with open("files/terminal.txt", "w") as f:
    f.write(result.stdout.decode())
    print(result.stdout.decode())
print("done")