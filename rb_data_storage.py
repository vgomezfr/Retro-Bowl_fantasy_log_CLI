import matplotlib.pyplot as plt

################################ GAME STATS AND SUBCLASSES ###############################
class Player_Game:
    def __init__(self, week, opponent, fum):
        self.week = week
        self.opponent = opponent
        self.fum = fum

    def calculate_passing_fpts(self):
        # 25 pass yd = 1 pt, 4pts per pass td, -2pts per int
        return round((0.04 * self.pass_yds) + (4 * self.pass_tds) - (2 * self.ints), ndigits=2)

    def calculate_rushing_fpts(self):
        return round((0.1 * self.rush_yds) + (6 * self.rush_tds), ndigits=2)
    
    def calculate_receiving_fpts(self):
        # PPR format
        return round((1 * self.rec) + (0.1 * self.rec_yds) + (6 * self.rec_tds), ndigits=2)

class Quarterback_Game(Player_Game):
    def __init__(self, week, opponent, cmp, att, pass_yds, pass_tds, pass_lng, ints,
                 sacks, carries, rush_yds, rush_tds, rush_lng, fum):
        
        super().__init__(week, opponent, fum)

        # Passing stats initialization
        self.att = att
        self.cmp = cmp
        self.cmp_pct = 0 if self.att == 0 else round(self.cmp / self.att, ndigits=2)
        self.pass_yds = pass_yds
        self.pass_tds = pass_tds
        self.pass_avg = 0 if self.att == 0 else round(self.pass_yds / self.att, ndigits=2)
        self.pass_lng = pass_lng
        self.ints = ints
        self.sacks = sacks

        # Rushing stats initialization
        self.carries = carries
        self.rush_yds = rush_yds
        self.rush_avg = 0 if self.carries == 0 else round(self.rush_yds / self.carries, ndigits=2)
        self.rush_tds = rush_tds
        self.rush_lng = rush_lng

        self.fpts = self.calculate_fpts()
    
    def calculate_fpts(self):
        return round(self.calculate_passing_fpts() + self.calculate_rushing_fpts() - (2 * self.fum), ndigits=2)

    def to_dict(self):
        return {
            "__type__": "Quarterback_Game",
            "week": self.week,
            "opponent": self.opponent,
            "att": self.att,
            "cmp": self.cmp,
            "pass_yds": self.pass_yds,
            "pass_tds": self.pass_tds,
            "pass_lng": self.pass_lng,
            "ints": self.ints,
            "sacks": self.sacks,
            "carries": self.carries,
            "rush_yds": self.rush_yds,
            "rush_tds": self.rush_tds,
            "rush_lng": self.rush_lng,
            "fum": self.fum
        }

    @classmethod
    def from_dict(cls, d: dict):
        return Quarterback_Game(d["week"], d["opponent"], d["cmp"], d["att"], 
                                d["pass_yds"], d["pass_tds"], d["pass_lng"], d["ints"], d["sacks"],
                                d["carries"], d["rush_yds"], d["rush_tds"], d["rush_lng"], d["fum"])

class Runningback_Game(Player_Game):
    def __init__(self, week, opponent, carries, rush_yds, rush_tds, rush_lng,
                 rec, rec_yds, rec_tds, rec_lng, fum):
        
        super().__init__(week, opponent, fum)

        # Rushing stats initialization
        self.carries = carries
        self.rush_yds = rush_yds
        self.rush_tds = rush_tds
        self.rush_avg = 0 if self.carries == 0 else round(self.rush_yds / self.carries, ndigits=2)
        self.rush_lng = rush_lng

        # Receiving stats initialization
        self.rec = rec
        self.rec_yds = rec_yds
        self.rec_tds = rec_tds
        self.rec_avg = 0 if self.rec == 0 else round(self.rec_yds / self.rec, ndigits=2)
        self.rec_lng = rec_lng

        self.fpts = self.calculate_fpts()
        

    def calculate_fpts(self):
        return round(self.calculate_rushing_fpts() + self.calculate_receiving_fpts() - (2 * self.fum), ndigits=2)

    def to_dict(self):
        return {
            "__type__": "Runningback_Game",
            "week": self.week,
            "opponent": self.opponent,
            "carries": self.carries,
            "rush_yds": self.rush_yds,
            "rush_tds": self.rush_tds,
            "rush_lng": self.rush_lng,
            "rec": self.rec,
            "rec_yds": self.rec_yds,
            "rec_tds": self.rec_tds,
            "rec_lng": self.rec_lng,
            "fum": self.fum,
            }

    @classmethod
    def from_dict(cls, d):
        return Runningback_Game(d["week"], d["opponent"], d["carries"], d["rush_yds"], d["rush_tds"],
                                d["rush_lng"], d["rec"], d["rec_yds"], d["rec_tds"], d["rec_lng"], d["fum"])

class Receiver_Game(Player_Game):
    def __init__(self, week: int, opponent: str, rec, rec_yds, rec_tds, rec_lng, fum):
        
        super().__init__(week, opponent, fum)

        self.rec = rec
        self.rec_yds = rec_yds
        self.rec_avg = 0 if self.rec == 0 else round(self.rec_yds / self.rec, ndigits=2)
        self.rec_tds = rec_tds
        self.rec_lng = rec_lng
        self.fpts = self.calculate_fpts()

    def __repr__(self):
        if type(self.week) == int:
            return f"Week {self.week} vs {self.opponent}"
        else:
            return f"{self.week} round vs {self.opponent}"

    def to_dict(self) -> dict:
        return {
            "__type__": "Receiver_Game",
            "week": self.week,
            "opponent": self.opponent,
            "rec": self.rec,
            "rec_yds": self.rec_yds,
            "rec_tds": self.rec_tds,
            "rec_lng": self.rec_lng,
            "fum": self.fum,
        }

    @classmethod
    def from_dict(cls, d):
        return Receiver_Game(d["week"], d["opponent"], d["rec"], d["rec_yds"], d["rec_tds"], d["rec_lng"], d["fum"])
    
    def calculate_fpts(self):
        return round(self.calculate_receiving_fpts() - (2 * self.fum), ndigits=2)

################################ SEASON RECORD AND SUBCLASSES ###############################
class Player_Season():
    def __init__(self, regular_season: list[Player_Game] = None, postseason: dict = None):
        if regular_season is not None:
            self.reg_season_games = regular_season
            self.num_reg_season_games = sum(1 for game in self.reg_season_games if game is not None)
        else:
            self.reg_season_games = [None] * 18
            self.num_reg_season_games = 0

        if postseason is not None:
            self.ps_games = postseason
            self.num_ps_games = sum(1 for v in self.ps_games.values() if v is not None)
        else:
            self.ps_games = {
                "wild card": None,
                "divisional": None,
                "conference": None,
                "super bowl": None
            }
            self.num_ps_games = 0

    def __repr__(self):
        if self.num_ps_games == 1:
            ps_phrase = "1 postseason game"
        else:
            ps_phrase = f"{self.num_ps_games} postseason games"
        return (f"Season with {self.num_reg_season_games} regular season games and " + ps_phrase)

    def to_dict(self):
        return {
            "__type__": "Player_Season",
            "reg_season": self.reg_season_games,
            "postseason": self.ps_games,
        }

    @classmethod
    def from_dict(cls, d):
        return Player_Season(d["reg_season"], d["postseason"])

################################ PLAYER CLASS AND SUBCLASSES ###############################
class Player:
    def __init__(self, name: str, position: str, retired: bool = False, career: list[Player_Season] = None):
        self.name = name
        self.position = position
        self.retired = retired

        if career is not None:
            self.career_stats = career
        else:
            self.career_stats = [Player_Season()]

    def __repr__(self):
        return f"{self.name}, {self.position}"

    def summary(self):
        experience = len(self.career_stats) - 1
        print(f"{self.name}, {self.position} with {experience} season(s) of experience")

    def _add_season(self):
        self.career_stats.append(Player_Season())

    def retire(self):
        self.retired = True

    def unretire(self):
        self.retired = False
    
    def _fetch_season(self, season: int) -> Player_Season:
        if not (season == -1 or 1 <= season <= len(self.career_stats)):
            raise KeyError("Season invalid. \n")
        return self.career_stats[-1] if season == -1 else self.career_stats[season - 1]

    def _fetch_game(self, season, week) -> Player_Game:
            # Pass in either an integer specifying the season number, or the entire season
            # Week is either an integer (regular season) or a string specifying playoff round
            if type(season) == int:
                season = self._fetch_season(season)

            if type(week) == int:
                if season.reg_season_games[week - 1] is None:
                    raise KeyError("Game not logged.")
                else:
                    return season.reg_season_games[week - 1]
            else:
                if season.ps_games[week] is None:
                    raise KeyError("Game not logged.")
                else:
                    return season.ps_games[week]

    def has_game_logged(self, season, week) -> bool:
        try:
            _ = self._fetch_game(season, week)
            return True
        except:
            return False
    
    def delete_game(self, season, week):
        if type(season) == int:
            season = self._fetch_season(season)

        if type(week) == int:
            if season.reg_season_games[week - 1] is None:
                raise KeyError("Game not logged.")
            else:
                season.reg_season_games[week - 1] = None
        else:
            if season.ps_games[week] is None:
                raise KeyError("Game not logged.")
            else:
                season.ps_games[week] = None

    def fetch_fantasy_season(self, season) -> tuple[list[float], float]:
        if type(season) == int:
            season = self._fetch_season(season)
        fseason = [game.fpts for game in season.reg_season_games if game is not None]
        season_fppg = sum(fseason) / len(fseason)
        return fseason, season_fppg

    def display_season_stats(self, season, include_ps: bool = False, plot: bool = True):
        def display_season_passing_stats(season: Player_Season, include_ps: bool):
            if season.num_reg_season_games == 0: 
                print("Season has no games logged. \n")
                return

            # Regular-season passing stats
            total_cmp = sum([game.cmp for game in season.reg_season_games if game is not None])
            total_att = sum([game.att for game in season.reg_season_games if game is not None])
            total_pass_yds = sum([game.pass_yds for game in season.reg_season_games if game is not None])
            total_pass_tds = sum([game.pass_tds for game in season.reg_season_games if game is not None])
            total_ints = sum([game.ints for game in season.reg_season_games if game is not None])

            # Add postseason stats if indicated
            if include_ps and season.num_ps_games > 0:
                # Postseason receiving stats
                total_cmp += sum([game.cmp for game in season.ps_games.values() if game is not None])
                total_att += sum([game.att for game in season.ps_games.values() if game is not None])
                total_pass_yds += sum([game.pass_yds for game in season.ps_games.values() if game is not None])
                total_pass_tds += sum([game.pass_tds for game in season.ps_games.values() if game is not None])
                total_ints += sum([game.ints for game in season.ps_games.values() if game is not None])

            # Season passing averages
            avg_cmp = round(total_cmp / num_games_played, ndigits=2)
            avg_att = round(total_att / num_games_played, ndigits=2)
            avg_pass_yds = round(total_pass_yds / num_games_played, ndigits=2)
            avg_pass_tds = round(total_pass_tds / num_games_played, ndigits=2)
            total_pass_avg = round(total_pass_yds / total_att, ndigits=2)
            total_cmp_pct = 0 if total_att == 0 else round(total_cmp / total_att, ndigits=2) * 100.0

            print(f"Season passing totals: {total_cmp}/{total_att} ({total_cmp_pct}%) for {total_pass_yds} yards and {total_pass_tds} touchdowns in {num_games_played} games, {total_pass_tds}/{total_ints} TD/Int")
            print(f"Season passing averages: {avg_cmp}/{avg_att} for {avg_pass_yds} yards and {avg_pass_tds} touchdowns per game at {total_pass_avg} yards per attempt")

        def display_season_rushing_stats(season: Player_Season, include_ps: bool):
            # Regular-season rushing stats
            total_carries = sum([game.carries for game in season.reg_season_games if game is not None])
            total_rush_yds = sum([game.rush_yds for game in season.reg_season_games if game is not None])
            total_rush_tds = sum([game.rush_tds for game in season.reg_season_games if game is not None])
    
            # Add postseason stats if indicated
            if include_ps:
                # Postseason rushing stats
                total_carries += sum([game.carries for game in season.ps_games.values() if game is not None])
                total_rush_yds += sum([game.rush_yds for game in season.ps_games.values() if game is not None])
                total_rush_tds += sum([game.rush_tds for game in season.ps_games.values() if game is not None])

            # Season rushing averages
            avg_carries = round(total_carries / num_games_played, ndigits=2)
            avg_rush_yds = round(total_rush_yds / num_games_played, ndigits=2)
            avg_rush_tds = round(total_rush_tds / num_games_played, ndigits=2)
            total_rush_avg = 0 if total_carries == 0 else round(total_rush_yds / total_carries, ndigits=2)

            print(f"Season rushing totals: {total_carries} carries for {total_rush_yds} yards and {total_rush_tds} touchdowns in {num_games_played} games")
            print(f"Season rushing averages: {avg_carries} carries for {avg_rush_yds} yards and {avg_rush_tds} touchdowns per game at {total_rush_avg} yards per carry")

        def display_season_receiving_stats(season: Player_Season, include_ps: bool):
            # Regular-season receiving stats
            total_rec = sum([game.rec for game in season.reg_season_games if game is not None])
            total_rec_yds = sum([game.rec_yds for game in season.reg_season_games if game is not None])
            total_rec_tds = sum([game.rec_tds for game in season.reg_season_games if game is not None])

            if include_ps:
                # Postseason receiving stats
                total_rec += sum([game.rec for game in season.ps_games.values() if game is not None])
                total_rec_yds += sum([game.rec_yds for game in season.ps_games.values() if game is not None])
                total_rec_tds += sum([game.rec_tds for game in season.ps_games.values() if game is not None])

            # Season receiving averages
            avg_rec = round(total_rec / num_games_played, ndigits=2)
            avg_rec_yds = round(total_rec_yds / num_games_played, ndigits=2)
            avg_rec_tds = round(total_rec_tds / num_games_played, ndigits=2)
            total_rec_avg = round(total_rec_yds / total_rec, ndigits=2)

            print(f"Season receiving totals: {total_rec} receptions for {total_rec_yds} yards and {total_rec_tds} touchdowns in {num_games_played} games")
            print(f"Season receiving averages: {avg_rec} receptions for {avg_rec_yds} yards and {avg_rec_tds} touchdowns per game at {total_rec_avg} yards per catch")

        def plot_fantasy_season(games_played: list, season_fpts: list[int], avg_fpts: int):
                plt.figure()

                # Use integer positions for plotting and annotating, so both share one coordinate system
                x_pos = list(range(len(games_played)))

                plt.plot(x_pos, season_fpts, marker="o", label="Fantasy Points", linestyle="-")

                # Relabel the ticks with the original week labels, including 'divisional'
                plt.xticks(x_pos, [str(g) for g in games_played])

                for xi, fscore in zip(x_pos, season_fpts):
                    trunc_score = f'{fscore:.2f}' if self.position == "QB" else f'{fscore:.1f}'
                    plt.annotate(
                        trunc_score,
                        (xi, fscore),              # annotate at the same position as the point
                        textcoords='offset points',
                        xytext=(0, 8),
                        ha='center'
                    )
                plt.axhline(y=avg_fpts, label="Season Average", color="orange", linestyle="--")
                plt.xlabel("Week")
                plt.ylabel("Fantasy Points Scored")
                plt.title(f"{self.name} Fantasy Points by Week")
        
                plt.legend()
                plt.show()
        
        if type(season) == int:
            season = self._fetch_season(season)

        games_played = [game.week for game in season.reg_season_games if game is not None]
        if include_ps:
            games_played.extend([game.week for game in season.ps_games.values() if game is not None])

        num_games_played = len(games_played)

        if num_games_played == 0:
            print("No games recorded in season. \n")
            return

        if self.position == "QB":
            display_season_passing_stats(season, include_ps)
            display_season_rushing_stats(season, include_ps)
        elif self.position == "RB":
            display_season_rushing_stats(season, include_ps)
            display_season_receiving_stats(season, include_ps)
        else: # WR or TE
            display_season_receiving_stats(season, include_ps)

        season_fpts = [game.fpts for game in season.reg_season_games if game is not None]
        if include_ps:
            season_fpts.extend([game.fpts for game in season.ps_games.values() if game is not None])

        total_fpts = round(sum(season_fpts), ndigits=2)
        avg_fpts = round(total_fpts / num_games_played, ndigits=2)

        print(f"Season fantasy stats: {total_fpts} fantasy points in {num_games_played} games, {avg_fpts} PPG")

        if plot:
            plot_fantasy_season(games_played, season_fpts, avg_fpts)

class Quarterback(Player):
    def __init__(self, name: str, position: str, retired: bool = False, career: list[Player_Season] = None):
        super().__init__(name, position, retired, career)

    def to_dict(self):
        return {
            "__type__": "Quarterback",
            "name": self.name,
            "position": self.position,
            "retired": self.retired,
            "career": self.career_stats
            }

    @classmethod
    def from_dict(cls, d: dict):
        return Quarterback(d["name"], d["position"], retired=d["retired"], career=d["career"])

    def add_game(self, week, opponent, att, cmp, pass_yds, pass_tds, pass_lng, ints, sacks,
                 carries, rush_yds, rush_tds, rush_lng, fum, season: int = -1) -> None:
        # Handle season gaps
        if season != -1:
            while len(self.career_stats) < season:
                self._add_season()
        else: # Season == -1
            if (type(week) == int):
                if self.career_stats[-1].num_ps_games > 0:
                    self._add_season()
                elif self.career_stats[-1].reg_season_games != [None] * 18:
                    for game in self.career_stats[-1].reg_season_games[::-1]:
                        if game is not None:
                            last_logged_game = game
                            break
                    if week < last_logged_game.week:
                        self.add_season

        season = self._fetch_season(season)

        game = Quarterback_Game(week, opponent, att, cmp, pass_yds, pass_tds, pass_lng, ints, sacks, 
                                carries, rush_yds, rush_tds, rush_lng, fum)
        
        if type(week) == int: # Regular season game
            if (season.reg_season_games[week - 1] is not None):
                raise KeyError("Game is already present. Use edit_game() to overwrite.")
            season.reg_season_games[week - 1] = game
            season.num_reg_season_games += 1
        
        elif type(week) == str: # Post-season game
            season.ps_games[week] = game
            season.num_ps_games += 1

    def display_game_stats(self, season, week):
        game = self._fetch_game(season, week)
        
        if type(game.week) == int:
            week_line = f"Week {game.week} vs {game.opponent}"
        else:
            week_line = f"{game.week} round vs {game.opponent}"


        if game.pass_tds == 1:
            pass_tds_line = "1 touchdown"
        else:
            pass_tds_line = f"{game.pass_tds} touchdowns"

        if game.rush_tds == 1:
            rush_tds_line = "1 touchdown"
        else:
            rush_tds_line = f"{game.rush_tds} touchdowns"

        out_lines = [
            week_line,
            f"{game.cmp} completions on {game.att} attempts for {game.pass_yds} yards and {pass_tds_line}",
            f"{game.pass_avg} yards per attempt",
            f"Longest passing play: {game.pass_lng} yards",
            f"{game.carries} carries for {game.rush_yds} yards and {rush_tds_line}",
            f"{game.rush_avg} yards per carry with a longest rush of {game.rush_lng} yards",
            f"Fumbles: {game.fum}",
            f"Fantasy points: {game.fpts}",
        ]
        output = "\n".join(out_lines)

        print(output)

class Runningback(Player):
    def __init__(self, name: str, position: str, retired: bool = False, career: list[Player_Season] = None):
        super().__init__(name, position, retired, career)

    def to_dict(self):
            return {
                "__type__": "Runningback",
                "name": self.name,
                "position": self.position,
                "retired": self.retired,
                "career": self.career_stats
                }

    @classmethod
    def from_dict(cls, d: dict):
        return Runningback(d["name"], d["position"], retired=d["retired"], career=d["career"])

    def add_game(self, week, opponent, carries, rush_yds, rush_tds, rush_lng,
                 rec, rec_yds, rec_tds, rec_lng, fum, season: int = -1) -> None:
    
        # Handle season gaps
        if season != -1:
            while len(self.career_stats) < season:
                self._add_season()
        else: # Season == -1
            if (type(week) == int):
                if self.career_stats[-1].num_ps_games > 0:
                    self._add_season()
                elif self.career_stats[-1].reg_season_games != [None] * 18:
                    for game in self.career_stats[-1].reg_season_games[::-1]:
                        if game is not None:
                            last_logged_game = game
                            break
                    if week < last_logged_game.week:
                        self.add_season

        season = self._fetch_season(season)

        game = Runningback_Game(week, opponent, carries, rush_yds, rush_tds, rush_lng, 
                                rec, rec_yds, rec_tds, rec_lng, fum)
        
        if type(week) == int: # Regular season game
            if (season.reg_season_games[week - 1] is not None):
                raise KeyError("Game is already present. Use edit_game() to overwrite.")
            season.reg_season_games[week - 1] = game
            season.num_reg_season_games += 1
        
        elif type(week) == str: # Post-season game
            season.ps_games[week] = game
            season.num_ps_games += 1

    def display_game_stats(self, season, week):
        game = self._fetch_game(season, week)
        
        if type(game.week) == int:
            week_line = f"Week {game.week} vs {game.opponent}"
        else:
            week_line = f"{game.week} round vs {game.opponent}"


        if game.rush_tds == 1:
            rush_tds_line = "1 rushing touchdown"
        else:
            rush_tds_line = f"{game.rush_tds} rushing touchdowns"

        if game.rec_tds == 1:
            
            rec_tds_line = "1 receiving touchdown"
        else:
            rec_tds_line = f"{game.rec_tds} receiving touchdowns"

        out_lines = [
            week_line,
            f"{game.carries} carries",
            f"{game.rush_yds} rushing yards",
            rush_tds_line,
            f"{game.rush_avg} yards per carry",
            f"Longest rush: {game.rush_lng} yards",
            f"{game.rec} receptions",
            f"{game.rec_yds} receiving yards",
            rec_tds_line,
            f"{game.rec_avg} yards per reception",
            f"Longest reception: {game.rec_lng} yards",
            f"Fumbles: {game.fum}",
            f"Fantasy points: {game.fpts}",
        ]
        output = "\n".join(out_lines)

        print(output)

# Receiver class applies to both WRs and TEs
class Receiver(Player):
    def __init__(self, name: str, position: str, retired: bool = False, career: list[Player_Season] = None):
        super().__init__(name, position, retired, career)

    def to_dict(self):
        return {
            "__type__": "Receiver",
            "name": self.name,
            "position": self.position,
            "retired": self.retired,
            "career": self.career_stats
            }

    @classmethod
    def from_dict(cls, d):
        return Receiver(d["name"], d["position"], retired=d["retired"], career=d["career"])

    def add_game(self, week, opponent: str, rec: int, rec_yds: int, rec_tds: int ,
                  rec_lng: int, fum: int, season: int = -1) -> None:

        # Handle season gaps
        if season != -1:
            while len(self.career_stats) < season:
                self._add_season()
        else: # Season == -1
            if (type(week) == int):
                if self.career_stats[-1].num_ps_games > 0:
                    self._add_season()
                elif self.career_stats[-1].reg_season_games != [None] * 18:
                    for game in self.career_stats[-1].reg_season_games[::-1]:
                        if game is not None:
                            last_logged_game = game
                            break
                    if week < last_logged_game.week:
                        self.add_season

        season = self._fetch_season(season)

        game = Receiver_Game(week, opponent, rec, rec_yds, rec_tds, rec_lng, fum)
        
        if type(week) == int: # Regular season game
            if (season.reg_season_games[week - 1] is not None):
                raise Exception("Game is already present. Use edit_game() to overwrite.")
            season.reg_season_games[week - 1] = game
            season.num_reg_season_games += 1

        elif type(week) == str: # Post-season game
            season.ps_games[week] = game
            season.num_ps_games += 1

    def display_game_stats(self, season, week):
        game = self._fetch_game(season, week)
        
        if type(game.week) == int:
            week_line = f"Week {game.week} vs {game.opponent}"
        else:
            week_line = f"{game.week} round vs {game.opponent}"

        if game.rec_tds == 1:
            tds_line = "1 receiving touchdown"
        else:
            tds_line = f"{game.rec_tds} receiving touchdowns"

        out_lines = [
            week_line,
            f"{game.rec} receptions for {game.rec_yds} receiving yards and {tds_line}",
            f"{game.rec_avg} yards per reception with a longest reception of {game.rec_lng} yards",
            f"Fantasy points: {game.fpts}",
        ]
        output = "\n".join(out_lines)

        print(output)
