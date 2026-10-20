from rb_data_storage import *

class Terminal:
    def __init__(self):
        self.players = dict()
        self.state = "main"
        self.action = None
        self.current_player = None

        # Map of valid actions at each terminal state
        self.valid_actions_map = {
        "main": {"P", "E", "V"},
        "player hub": {"L", "D", "R", "S", "P", "X", "Z", "E"},  
        }

        # Prompts to be shown at corresponding terminal states
        self.prompts = {
        "main": "Choose player [P]     Display player list [V]     Exit [E] \n",
        "player hub": "Log game [L]     Delete game [D]     Retrieve game [R]     Season stats [S] \nChoose different player[P]     Delete this player [X]     Retire this player [Z]     Exit [E] \n",
        }

        # Reprompts to be shown when invalid action is inputted at terminal state
        self.reprompts = {
        "main": "Enter P to choose a player, V to display player list, or E to exit \n",
        "player hub": "Enter L to enter a game, D to delete a game, R to retrieve game data, S to retrieve season data, \nP to access a different player, X to delete this player, Z to retire this player, or E to exit. \n",
        }

        # Map of actions to be taken upon corresponding terminal input
        self.action_functions_map = {
            "V": self.display_known_players,
            "P": self.choose_player,
            "X": self.delete_player,
            "Z": self.retire_player,
            "L": self.log_game,
            "D": self.delete_game,
            "R": self.display_game,
            "S": self.display_season,
            "E": self.exit
        }

        # Defining valid inputs for game weeks
        self.ps_input_map = {
            "WC": {"wc", "WC", "wild card", "Wild card", "Wild Card", "wildcard", "Wildcard"},
            "D": {"division", "Division", "divisional", "Divisional", "d", "D"},
            "C": {"conference", "Conference", "NFC", "AFC", "nfc", "afc", "c", "C"},
            "SB": {"super bowl", "Super bowl", "Super Bowl", "superbowl", "Superbowl", "sb", "SB"}
        }

        self.valid_ps_game_inputs = set()
        for valid_input_set in self.ps_input_map.values():
            self.valid_ps_game_inputs = self.valid_ps_game_inputs.union(valid_input_set)
        
        self.valid_week_inputs = self.valid_ps_game_inputs.union(set([str(v) for v in list(range(1, 19))]))

    def request_stat(self, prompt: str, neg_possible: bool = False) -> int:
        stat_value = ""
        while type(stat_value) != int:
            stat_value = input(prompt + "? \n")
            try:
                stat_value = int(stat_value)
                if not neg_possible and stat_value < 0:
                    print("This stat cannot be negative; please input a positive value (or 0).")
                    stat_value = ""
            except:
                print("Please input an integer.")
                continue
        return stat_value

    def request_confirmation(self, prompt: str) -> bool:
        confirmation = ""
        while not (confirmation == "Y" or confirmation == "y" or
                   confirmation == "N" or confirmation == "n"):
            confirmation = input(prompt + " [Y]/[N] \n")
        
        return True if (confirmation == "Y" or confirmation == "y") else 0

    def retrieve_ps_round(self, week: str) -> str:
        """
        Guaranteed that week is a valid entry in exactly one of the sets 
        which make up the values of self.ps_input_map, we return that set's key
        """
        for ps_round in self.ps_input_map.keys():
            if week in self.ps_input_map[ps_round]:
                return ps_round

    def request_week(self):
        """
        Prompts user input for the desired week until a valid input is given.
        Guaranteed to return either (1) a string that maps to a postseason round
        or (2) an integer between 1 and 18.
        """
        week = input("Week? \n")
        while week not in self.valid_week_inputs:
            week = input("Enter a number 1-18 for regular season game or playoff round for postseason game. \n")

        if week in self.valid_ps_game_inputs:
            week = self.retrieve_ps_round(week)
        else:
            # Week is an integer between 1 and 18
            week = int(week)

        return week

    def request_season(self):
        """
        Prompts user input until it receives a valid season number.
        Guaranteed to return either -1 or a positive integer.
        """
        season = 0 # Dummy value to begin while loop
        while not (type(season) == int and (season == -1 or season >= 1)):
            season = input("Enter season number or -1 for most recent season. \n")
            try:
                season = int(season)
            except:
                print("Please input an integer.")
                continue
        
        return season
    
    def valid_actions(self) -> set:
        return self.valid_actions_map[self.state]

    def is_valid_action(self) -> bool:
        return (self.action in self.valid_actions())

    def request_action(self, reprompt=False) -> None:
        """
        Prompts (and reprompts) user until a valid action is input.
        At return, the terminal has a valid action fitting its state.
        """
        if reprompt:
            self.action = input(self.reprompts[self.state])
        else:
            self.action = input(self.prompts[self.state])

        if not self.is_valid_action():
            self.request_action(reprompt=True)

    def perform_action(self):
        self.action_functions_map[self.action]()

    def display_known_players(self):
        active_players = []
        retired_players = []
        for player_name, player in zip(self.players.keys(), self.players.values()):
            if player.retired:
                retired_players.append(player_name)
            else:
                active_players.append(player_name)

        print("Active players:", active_players)
        print("Retired players:", retired_players)

    def create_player(self, player_name: str) -> None:
        # Adds a Player of the inputted name and position to the player dictionary
        position = input("Create new player. Position? \n")

        if position == "WR" or position == "TE":
            self.players[player_name] = Receiver(player_name, position)
        elif position == "RB":
            self.players[player_name] = Runningback(player_name, position)
        elif position == "QB":
            self.players[player_name] = Quarterback(player_name, position)
        
        print(f"Player {player_name} added to registry.")

    def choose_player(self):
        # Player selection
        player_name = input("Player name? \n")

        if self.players.get(player_name) is None:
            confirm_new_player = self.request_confirmation("Player name not in database. Create new player?")
            if confirm_new_player:
                self.create_player(player_name)
            else:
                return

        self.current_player = self.players[player_name]
        self.state = "player hub"

    def delete_player(self):
        # Player deletion
        confirm_delete_player = self.request_confirmation(f"Are you sure you want to delete player {self.current_player.name}? \n")
        if confirm_delete_player:
            self.players.pop(self.current_player.name)
            print(f"Player {self.current_player.name} deleted. Returning to main menu. \n")
            self.state = "main"
        else:
            print("Player deletion canceled. \n")
            # self.state remains "player_hub"
    
    def retire_player(self):
        """
        Retire/unretire a player depending on their current retirement status.
        """
        if self.current_player.retired:
            confirm_unretire_player = self.request_confirmation("Player already retired. Unretire player?")
            if confirm_unretire_player:
                self.current_player.unretire()
                print(f"Player {self.current_player.name} unretired. \n")
            else:
                print("Player unretirement canceled. \n")
        else:
            # Retire player
            retirement_prompt = [
                f"Are you sure you want to retire player {self.current_player.name}?", 
                "You will no longer be able to log new games for this player, but can still view stats."
                ]
            retirement_prompt = "\n".join(retirement_prompt)
            
            confirm_retire_player = self.request_confirmation(retirement_prompt)
            if confirm_retire_player:
                self.current_player.retire()
                print(f"Player {self.current_player.name} retired. \n")
            else:
                print("Player retirement canceled. \n")

    def log_game(self):
        """
        Prompts user input and creates a new Player_Game object in the current player's career
        """
        player = self.current_player

        if player.retired:
            print("Cannot log new games for retired players. \n")
            return

        season = self.request_season()
        week = self.request_week()

        if player.has_game_logged(season, week):
            print("Game already logged. Try viewing stats or deleting the logged game.")
            return

        opponent = input("Opponent? \n")

        # Get input for appropriate game stats

        if player.position == "QB":
            cmp = self.request_stat("Passes completed")
            att = self.request_stat("Passes attempted")
            pass_yds = self.request_stat("Passing yards", neg_possible=True)
            pass_tds = self.request_stat("Passing touchdowns")
            pass_lng = self.request_stat("Longest passing play", neg_possible=True)
            ints = self.request_stat("Interceptions")
            sacks = self.request_stat("Sacks")

        if player.position == "QB" or player.position == "RB":
            # Input rushing stats
            carries = self.request_stat("Carries")
            rush_yds = self.request_stat("Rushing yards", neg_possible=True)
            rush_tds = self.request_stat("Rushing touchdowns")
            rush_lng = self.request_stat("Longest rush", neg_possible=True)

        if player.position == "RB" or player.position == "WR" or player.position == "TE":
            # Input passing stats
            rec = self.request_stat("Receptions")
            rec_yds = self.request_stat("Receiving yards", neg_possible=True)
            rec_tds = self.request_stat("Receiving touchdowns")
            rec_lng = self.request_stat("Longest reception", neg_possible=True)

        fum = self.request_stat("Fumbles")

        # Pack all relevant game stats into a tuple and pass that argument tuple into player.add_game()
        if player.position == "QB":
            game_stats = (cmp, att, pass_yds, pass_tds, pass_lng, ints, sacks, carries, rush_yds, rush_tds, rush_lng, fum)
        elif player.position == "RB":
            game_stats = (carries, rush_yds, rush_tds, rush_lng, rec, rec_yds, rec_tds, rec_lng, fum)
        else:
            game_stats = (rec, rec_yds, rec_tds, rec_lng, fum)
        
        player.add_game(week, opponent, *game_stats, season)

    def delete_game(self):
        season = self.request_season()
        week = self.request_week()

        if self.current_player.has_game_logged(season, week):
            confirm_delete_game = self.request_confirmation("Are you sure you want to delete this game? This action cannot be undone.")
            if confirm_delete_game:
                self.current_player.delete_game(season, week)
                print("Game deleted. \n")
            else:
                print("Game deletion canceled. \n")
        else:
            print("Cannot delete a game where there is no data logged. \n")

    def display_game(self):
        season = self.request_season()
        week = self.request_week()

        if self.current_player.has_game_logged(season, week):
            self.current_player.display_game_stats(season, week)
        else:
            print("No data logged for that game. \n")

    def display_season(self):
        season = self.request_season()
        while season > len(self.current_player.career_stats):
            print(f"Season out of range: Player does not have {season} seasons logged.")
            season = self.request_season()

        include_ps = self.request_confirmation("Include postseason?")

        self.current_player.display_season_stats(season, include_ps)     

    def exit(self):
        pass   
