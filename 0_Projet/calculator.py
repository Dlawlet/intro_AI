import pandas as pd

#Usefull functions
def print_parsed_data(game_stats, key):

    # Print the parsed game data
    for stat in game_stats:
        print(f"First player: {stat['First player']}")
        print(f"Second player: {stat['Second player']}")
        print(f"{key}: {stat[key]}")
        print("\n")

#Function that read the stat.txt file to know the win rate of the first player on the second player
def parse_stats(filename):
    # Initialize an empty list to store the parsed game data
    game_stats = []

    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if '#' in line:
            # Split the line into components
            components = line.split("#")

            first_player = components[1]
            second_player = components[3]
            winner = components[5]

            # Add the game data to the list
            game_stats.append({"First player": first_player,
                               "Second player": second_player,
                               "Winner": winner})

    return game_stats
def calculate_win_rate(game_stats):
    #ATTENTION, AFIN DE SIMPLIFIER LE CODE, ON PART DE L'IDEE QUE LE FIRST_PLAYER EST TOUJOURS LE MEME (pareil pour second_player)
    first_player_win_count = 0
    second_player_win_count = 0
    for stat in game_stats:
        first_player = stat["First player"]
        second_player = stat["Second player"]
        winner = stat["Winner"]

        if winner == "RED":
            first_player_win_count += 1
        elif winner == "BLUE":
            second_player_win_count += 1
    total = first_player_win_count + second_player_win_count
    win_rate = (first_player_win_count / total)

    win_rate_string = f"The #{first_player}# win rate on #{second_player}# is #{win_rate}#"
    return win_rate_string,win_rate
def write_win_rate_to_file(win_rate_string,access_mode="a"):
    with open("files/win_rate.txt", access_mode) as f:
        f.write(win_rate_string+"\n")
def translate_stat_to_win_rate(to_write):
    filename = "files/stat.txt"
    game_stats = parse_stats(filename)
    #print_parsed_data(game_stats, "Winner")
    win_rate_string, _ = calculate_win_rate(game_stats)
    if to_write:
        write_win_rate_to_file(win_rate_string)


#Function that read the win_rate.txt file to know all the win rates.
def parse_win_rate(filename):
    # Initialize an empty list to store the parsed game data
    win_rate_stats = []

    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if '#' in line:
            # Split the line into components
            components = line.split("#")

            first_player = components[1]
            second_player = components[3]
            win_rate = components[5]

            # Add the game data to the list
            win_rate_stats.append({"First player": first_player,
                               "Second player": second_player,
                               "Win Rate": win_rate})

    return win_rate_stats
def display_win_rate_matrix(win_rate_stats):
    # Initialize an empty dictionary for the matrix
    win_rate_matrix = {}

    for stat in win_rate_stats:
        player = stat['First player']
        opponent = stat['Second player']
        win_rate = float(stat['Win Rate'])

        # If the player is not yet in the matrix, add them
        if player not in win_rate_matrix:
            win_rate_matrix[player] = {}

        # Add the win rate against the opponent to the player's row
        win_rate_matrix[player][opponent] = win_rate

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(win_rate_matrix)

    # Print the DataFrame
    print(df)
def translate_win_rate_to_matrix():
    filename = "files/win_rate.txt"
    win_rate_stats = parse_win_rate(filename)
    display_win_rate_matrix(win_rate_stats)

translate_stat_to_win_rate(to_write=False)
translate_win_rate_to_matrix()



