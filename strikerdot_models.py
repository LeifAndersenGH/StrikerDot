

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
    def __init__(self, team1, team2, time, elem=None):
        self.team1 = team1
        self.team2 = team2
        self.time = time
        self.elem = elem
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
    def CreateBasicFromRawData_Strikerdot(data):
        elem = data[-1]
        teams = data[0]
        details = data[1]

        team1, team2 = teams.split('\n')
        score, time = details.split('\n')
        
        team1 = Team(team1)
        team2 = Team(team2)
        
        team1.score, team2.score = score.split('--')
        try:
            quater, time = time.split()
        except:
            quater, num, time = time.split()
            
        time = GameTime(quater, time)
        game = Game(team1, team2, time, elem)
        return game





### An object about a team. Includes the score of the current game and the team name
class Team(object):
    def __init__(self, name, score=0):
        self.name = name
        self.score = int(score)
        
    def __str__(self):
        return 'Team: name=%s, score=%s' % (self.name, self.score)


## An object that describes the time left in a game
class GameTime(object):
    def __init__(self, quater, time):
        self.quater = quater
        self.time = time
        
    def __str__(self):
        return self.quater + " " + self.time



## And objec that describes a games bet
class Bet(object):
    pass







# Create a basic model from raw data scrapped from strikerdot
def CreateBasicModelsFromRawData_Stikerdot(data):
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
