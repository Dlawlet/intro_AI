import subprocess

def read_last_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if lines:
            last_line = lines[-1].strip()
            return last_line
        else:
            return None

def run_tes():      
    # Run a command in the terminal
    cmd = "python3 main.py"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

    # Capture the output and write it to a file
    with open("files/terminal.txt", "w") as f:
        f.write(result.stdout.decode())
        #print(result.stdout.decode())
    with open("files/stat.txt", "a") as f:
        f.write(read_last_line("files/terminal.txt")+"\n")

    print("done")

for _ in range(1):
    run_tes()