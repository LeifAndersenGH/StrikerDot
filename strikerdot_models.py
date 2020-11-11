

## Models Module

## This file is simply to create organized models of data
## There is also a few methods at the bottom used to convert raw data to models along with a corresponding static method for that model.


## A league has a name like NFL and a list of games.
class League(object):
    def __init__(self, name):
        self.name = name
        self.games = []
    
    def add_game(self, game):
        self.games += [game]
        
    def __str__(self):
        return "<League: %s, Games=%d" % (self.name, len(self.games))



## A game holds two Team() objects, a GameTime() object and a list of Bets()s
## -- title() - Returns team1.name vs team2.name
## -- currently_winning() - Returns the currently winning team object
## -- is_tied() - Returns True or False
## -- add_bet(bet) - Adds a bet to the games list of bets
class Game(object):
    def __init__(self, team1, team2, time):
        self.team1 = team1
        self.team2 = team2
        self.time = time
        self.bets = []
        
    def __str__(self):
        return  self.title() + " : " + self.score_as_string() + " : " + str(self.time)
    
    def teams(self):
        return [self.team1, self.team2]
    
    def team_names(self):
        return [self.team1.name, self.team2.name]    
    
    def title(self):
        return self.team1.name + " vs " + self.team2.name
    
    def score (self):
        return [self.team1.score, self.team2.score]
    
    def score_as_string(self):
        return self.team1.score + " - " + self.team2.score
        
    
    def currently_winning(self):
        leading = None
        if (self.team1.score > self.team2.score):
            leading = self.team1
        elif (self.team1.score < self.team2.score):
            leading = self.team2
        return leading
    
    def is_tied(self):
        return self.team1.score == self.team2.score
    
    def add_bet(self, game):
        pass
    
    
    
    
    ## Create a basic model from raw data given by strikerdot.com. First layer of scraping.
    @staticmethod
    def CreateBasicFromLiveRawData_Strikerdot(data):
        teams = data[0]
        details = data[1]

        team1, team2 = teams.split('\n')
        score, time = details.split('\n')
        
        team1 = LiveTeam(team1)
        team2 = LiveTeam(team2)
        
        team1.score, team2.score = score.split('--')
        
        # Exception catches overtime
        try: quater, time = time.split()
        except: quater, num, time = time.split()
            
        time = GameTime(quater, time)
        game = Game(team1, team2, time)
        return game
    
    @staticmethod
    def CreateBasicFromStraightRawData_Strikerdot(date, raw_data):
        # raw_data = [broadcastChannel, time, team1_data, team2_data],
        # team1 or team2 = [name, spread, money_line, total_points]
        
        broadcast_channel = raw_data[0]
        time = raw_data[1]
        
        team1_data = raw_data[2]
        team2_data= raw_data[3]
        
        # team1 or team2 = [team_name, spread, money_line, total_points]
        team1_spread_bet = SpreadBet.CreateFromStraightData(team1_data[0], team1_data[1]) 
        team2_spread_bet = SpreadBet.CreateFromStraightData(team2_data[0], team2_data[1])
        
        team1_ml_bet = MoneyLineBet.CreateFromStraightData(team1_data[0], team1_data[2]) 
        team2_ml_bet = MoneyLineBet.CreateFromStraightData(team2_data[0], team2_data[2])
        
        team1_tp_bet = TotalPointsBet.CreateFromStraightData(team1_data[0], team1_data[3]) 
        team2_tp_bet = TotalPointsBet.CreateFromStraightData(team2_data[0], team2_data[3])
        
        team1 = StraightTeam(team1_data)
        team2 = StraightTeam(team2_data)
        
        
        team1.score, team2.score = score.split('--')
        try:
            quater, time = time.split()
        except:
            quater, num, time = time.split()
            
        time = GameTime(quater, time)
        game = Game(team1, team2, time, elem)
        return game




### An object about a team. Includes the score of the current game and the team name
class LiveTeam(object):
    def __init__(self, name, score=0):
        self.name = name
        self.score = int(score)
        
    def __str__(self):
        return 'Team: name=%s, score=%s' % (self.name, self.score)



class StraightTeam(object):
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return 'Team: name=%s' % (self.name)
        
        

## An object that describes the time left in a game
class GameTime(object):
    def __init__(self, quater, time):
        self.quater = quater
        self.time = time
        
    def __str__(self):
        return self.quater + " " + self.time



## And objec that describes a games bet
class Bet(object):
    def __init__(self, name, team_name):
        self.name = name
        self.team_name = team_name

class StraightBet(Bet):
    def __init__(self, name, team_name):
        super(StraightBet, self).__init__(name, team_name)


class SpreadBet(Bet):
    def __init__(self, team_name, spread, odds):
        super(Spread, self).__init__("SpreadBet", team_name)
        self.team = team_name
        self.spread = spread
        self.odds = odds
        
    @staticmethod
    def CreateFromStraightData(team_name, data):
        spread, odds = data.split()
        SpreadBet()
        
        








# Create a basic model from raw data scrapped from strikerdot
def CreateBasicModelsFromLiveRawData_Stikerdot(data):
    leagues = []
    
    print("CreateBasicModelsFromRawData_Stikerdot")
    print()
    # Create leagues from the data
    for league_name, raw_games in data.items():
        print("\t League: ", league_name)
        league = League(league_name)
        leagues += [league]
        
        #
        for raw_game in raw_games:
            game = Game.CreateBasicFromRawData_Strikerdot(raw_game)
            league.add_game(game)
            print("\t\t Game: ", game)
            
    print("\n CreateBasicModelsFromRawData_Stikerdot DONEDONE \n\n")                        
    return leagues





def CreateBasicModelsFromStraightRawData_Stikerdot(data):
    # Data structure example
    # data = {
        # date1: [
        #     [broadcastChannel, time, team1_data, team2_data],
        #     [broadcastChannel, time, team1_data, team2_data],
        #     [broadcastChannel, time, team1_data, team2_data],
        # ], 
        # date2: [
        #     [broadcastChannel, time, team1_data, team2_data],
        #     [broadcastChannel, time, team1_data, team2_data],
        #     [broadcastChannel, time, team1_data, team2_data],
        #     [broadcastChannel, time, team1_data, team2_data],
        #     [broadcastChannel, time, team1_data, team2_data],
        # ],        
    # }
    
    games = []
    for date, raw_game_data in data.items():
        game = Game.CreateBasicFromStraightRawData_Strikerdot(date, raw_game_data)

    return games
    
    
    
    