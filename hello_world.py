import json
from colorama import init, Fore, Style

init(autoreset=True)

def collect_participants():
    names = input("Enter participant names (comma-separated): ").split(",")
    return [name.strip() for name in names]

def collect_predictions(participants, rounds):
    predictions = {}

    for name in participants:
        print(Fore.CYAN + f"\n🕯️ Enter predictions for {name}:")
        predictions[name] = {}

        # Wildcard Round
        wildcard_matchups = [
            ("Tigers", "Guardians"),
            ("Red Sox", "Yankees"),
            ("Padres", "Cubs"),
            ("Reds", "Dodgers")
        ]
        predictions[name]["Wildcard Round"] = []
        for team1, team2 in wildcard_matchups:
            print(f"Wildcard Round - {team1} vs {team2}")
            pick = input("Your pick: ").strip()
            predictions[name]["Wildcard Round"].append(pick)

        # Divisional Round (using predicted Wildcard winners)
        wc_winners = predictions[name]["Wildcard Round"]
        divisional_matchups = [
            (wc_winners[0], "Mariners"),
            (wc_winners[1], "Blue Jays"),
            (wc_winners[2], "Brewers"),
            (wc_winners[3], "Phillies")
        ]
        predictions[name]["Divisional Round"] = []
        for team1, team2 in divisional_matchups:
            print(f"Divisional Round - {team1} vs {team2}")
            pick = input("Your pick: ").strip()
            predictions[name]["Divisional Round"].append(pick)

        # Conference Finals (using predicted Divisional winners)
        div_winners = predictions[name]["Divisional Round"]
        conference_matchups = [
            (div_winners[0], div_winners[1]),  # ALCS
            (div_winners[2], div_winners[3])   # NLCS
        ]
        predictions[name]["Conference Finals"] = []
        for team1, team2 in conference_matchups:
            print(f"Conference Finals - {team1} vs {team2}")
            pick = input("Your pick: ").strip()
            predictions[name]["Conference Finals"].append(pick)

        # World Series (using predicted Conference winners)
        conf_winners = predictions[name]["Conference Finals"]
        world_series_matchup = [(conf_winners[0], conf_winners[1])]
        predictions[name]["World Series"] = []
        for team1, team2 in world_series_matchup:
            print(f"World Series - {team1} vs {team2}")
            pick = input("Your pick: ").strip()
            predictions[name]["World Series"].append(pick)

    return predictions



def collect_results(rounds):
    results = {}

    # Wildcard Round
    print(Fore.YELLOW + "\n🔥 Enter actual results for Wildcard Round:")
    results["Wildcard Round"] = []
    for team1, team2 in rounds["Wildcard Round"]:
        print(f"{team1} vs {team2}")
        winner = input("Winner: ").strip()
        results["Wildcard Round"].append(winner)

    # Divisional Round (using actual Wildcard winners)
    wc_winners = results["Wildcard Round"]
    divisional_matchups = [
        (wc_winners[0], "Mariners"),
        (wc_winners[1], "Blue Jays"),
        (wc_winners[2], "Brewers"),
        (wc_winners[3], "Phillies")
    ]
    rounds["Divisional Round"] = divisional_matchups
    print(Fore.YELLOW + "\n🔥 Enter actual results for Divisional Round:")
    results["Divisional Round"] = []
    for team1, team2 in divisional_matchups:
        print(f"{team1} vs {team2}")
        winner = input("Winner: ").strip()
        results["Divisional Round"].append(winner)

    # Conference Finals
    div_winners = results["Divisional Round"]
    conference_matchups = [
        (div_winners[0], div_winners[1]),
        (div_winners[2], div_winners[3])
    ]
    rounds["Conference Finals"] = conference_matchups
    print(Fore.YELLOW + "\n🔥 Enter actual results for Conference Finals:")
    results["Conference Finals"] = []
    for team1, team2 in conference_matchups:
        print(f"{team1} vs {team2}")
        winner = input("Winner: ").strip()
        results["Conference Finals"].append(winner)

    # World Series
    conf_winners = results["Conference Finals"]
    world_series_matchup = [(conf_winners[0], conf_winners[1])]
    rounds["World Series"] = world_series_matchup
    print(Fore.YELLOW + "\n🔥 Enter actual result for World Series:")
    results["World Series"] = []
    for team1, team2 in world_series_matchup:
        print(f"{team1} vs {team2}")
        winner = input("Winner: ").strip()
        results["World Series"].append(winner)

    return results

def generate_next_round(previous_winners):
    return [(previous_winners[i], previous_winners[i+1]) for i in range(0, len(previous_winners), 2)]

def calculate_standings(predictions, results):
    standings = {}
    for name, user_rounds in predictions.items():
        wins = 0
        losses = 0
        for round_name in results:
            actuals = results[round_name]
            picks = user_rounds.get(round_name, [])
            for pick, actual in zip(picks, actuals):
                if pick == actual:
                    wins += 1
                else:
                    losses += 1
        total_games = wins + losses
        standings[name] = {
            "Wins": wins,
            "Losses": losses,
            "Remaining": sum(len(v) for v in results.values()) - total_games
        }
    return standings

def display_standings(standings):
    print(Fore.MAGENTA + "\n📜 Final Standings 📜")
    for name, record in standings.items():
        print(f"{name}: {record['Wins']} Wins / {record['Losses']} Losses / {record['Remaining']} Remaining")

def save_predictions_to_file(predictions, filename="predictions.json"):
    with open(filename, "w") as f:
        json.dump(predictions, f, indent=4)
    print(Fore.GREEN + "✅ Predictions saved to database.")

def load_predictions_from_file(filename="predictions.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(Fore.RED + "⚠️ No saved predictions found.")
        return {}

def advance_round(rounds, results, current_round, next_round):
    if current_round in results:
        winners = results[current_round]
        next_matchups = [(winners[i], winners[i+1]) for i in range(0, len(winners), 2)]
        rounds[next_round] = next_matchups
        print(Fore.GREEN + f"\n🧭 {next_round} matchups generated from {current_round} results.")

def main_menu():
    rounds = {
        "Wildcard Round": [
            ("Tigers", "Guardians"),
            ("Red Sox", "Yankees"),
            ("Padres", "Cubs"),
            ("Reds", "Dodgers")
        ]
    }

    predictions = {}
    results = {}
    participants = []

    while True:
        print(Fore.BLUE + "\n⚾ MLB Playoff Tracker Menu ⚾")
        print("1. Enter participant names")
        print("2. Enter predictions")
        print("3. Enter actual results")
        print("4. View standings")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            participants = collect_participants()

        elif choice == "2":
            if not participants:
                print(Fore.YELLOW + "Please enter participant names first.")
            else:
                predictions = collect_predictions(participants, rounds)
                save_predictions_to_file(predictions)

        elif choice == "3":
            results.update(collect_results(rounds))
            advance_round(rounds, results, "Wildcard Round", "Divisional Round")
            advance_round(rounds, results, "Divisional Round", "Conference Finals")
            advance_round(rounds, results, "Conference Finals", "World Series")

            if "Wildcard Round" in results and "Divisional Round" not in rounds:
                wc_winners = results["Wildcard Round"]
                rounds["Divisional Round"] = [
                    (wc_winners[0], "Mariners"),
                    (wc_winners[1], "Blue Jays"),
                    (wc_winners[2], "Brewers"),
                    (wc_winners[3], "Phillies")
                ]
                print(Fore.GREEN + "\n🧭 Divisional Round matchups generated.")

            if "Divisional Round" in results and "Conference Finals" not in rounds:
                div_winners = results["Divisional Round"]
                rounds["Conference Finals"] = generate_next_round(div_winners)
                print(Fore.GREEN + "\n🧭 Conference Finals matchups generated.")

            if "Conference Finals" in results and "World Series" not in rounds:
                conf_winners = results["Conference Finals"]
                rounds["World Series"] = [(conf_winners[0], conf_winners[1])]
                print(Fore.GREEN + "\n🧭 World Series matchup generated.")

        elif choice == "4":
            predictions = load_predictions_from_file()
            if not predictions or not results:
                print(Fore.YELLOW + "Please enter predictions and results first.")
            else:
                standings = calculate_standings(predictions, results)
                display_standings(standings)

        elif choice == "5":
            print(Fore.CYAN + "Exiting the ritual chamber. May your predictions be luminous.")
            break

        else:
            print(Fore.RED + "Invalid choice. Please select a valid threshold.")

# Begin the ritual
main_menu()
