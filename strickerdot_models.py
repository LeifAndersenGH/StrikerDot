

class League(object):
    def __init__(self, name):
        self.name = name
        self.games = []
    
    def add_game(self, game):
        self.games += [game]



class Game(object):
    def __init__(self, team1, team2, time):
        self.team1 = team1
        self.team2 = team2
        self.time = time
        self.bets = []
        
    def __str__(self):
        score = self.team1.score + " - " + self.team2.score
        return self.team1.name + " vs " + self.team2.name + " : " + score + " : " + str(self.time)
    
    def get_score (self):
        return [self.team1.score, self.team2.score]
    
    def currently_winning(self):
        leading = None
        if (self.team1.score > self.team2.score):
            leading = self.team1
        elif (self.team2.score > self.team1.score):
            leading = self.team2
        return leading
    
    def is_tied(self):
        return self.team1.score == self.team2.score
    
    def add_bet(self, game):
        pass
    
    @staticmethod
    def CreateFromRawData(data):
        teams = data[0]
        details = data[1]

        team1, team2 = teams.split('\n')
        score, time = details.split('\n')
        
        team1 = Team(team1)
        team2 = Team(team2)
        
        team1.score, team2.score = score.split('--')
        quater, time = time.split()
        time = GameTime(quater, time)
        return Game(team1, team2, time)


class Team(object):
    def __init__(self, name, score=0):
        self.name = name
        self.score = int(score)
        
    def __str__(self):
        return 'Team: name=%s, score=%s' % (self.name, self.score)


class GameTime(object):
    def __init__(self, quater, time):
        self.quater = quater
        self.time = time
        
    def __str__(self):
        return self.quater + " " + self.time


class Bet(object):
    pass


