import time
import pprint
from actions import Login, ScrapeLeaguesAndGamesLIVE, ScrapeLeaguesAndGamesStraight
from selenium_handler import StrikerdotHandler
from strikerdot_models import CreateBasicModelsFromLiveRawData_Stikerdot, CreateBasicModelsFromStraightRawData_Stikerdot


def Scrape(handler):
    print ("\nFUNCTION: Scrape")
    print("\n[*] Action - Scraping...")
           
    # Scrape the Football Leagues and there games.
    data = handler.actions['ScrapeLeaguesAndGamesLIVE'].invoke()
    
    # Using the scraped data begin to generate objects and fill them with information
    leagues = CreateBasicModelsFromLiveRawData_Stikerdot(data)
    
    print (leagues)
    for league in leagues:
        print (league)
        for game in league.games:
            print(game)
    
    print ("END FUNCTION: Scrape\n") 
    return



def LoopScraper(handler, time_left, times_to_update, update_time, delta_time):
    # Subtract the amount of time thas has passed from our timer that will let us scrape again.
    time_left -= delta_time;
    
    # If the timer has 0 seconds left on it Reset the timer and Scrape.
    if (time_left <= 0):

        times_to_update -= 1
        time_left = update_time # Reset the time

        Scrape(handler)  
    return [handler, time_left, times_to_update, update_time, delta_time]




def CalculateTime(last_time):   
    # Calculate the amount of time that has passed since last here
    # Tracks how long it has been since we were last here and use that as a bases to calculate a second
    # delta_time == Time passed since last here
    delta_time = time.time() - last_time 
    # Reset last_time we were here to now
    last_time = time.time()
    return [delta_time, last_time]



def CreateHandler(redirect = False):
    
    # Create a browser
    handler = StrikerdotHandler()
    
    
    # Add all of actions that will happen
    handler.add_action(Login)
    # Nothing has happened yet
    
    handler.login(redirect)
        
    if not handler.is_logged_in:
        print ("[-] Failed.")
        return handler

    return handler


def LiveBetMain():
    
    handler = CreateHandler()
    handler.add_action(ScrapeLeaguesAndGamesLIVE)
    
    update_time = 30 # Update every seconds
    time_left = 0

    start_time = time.time()
    time.sleep(3)
    
    last_time = time.time()
    delta_time = 0
    
    times_to_update = 1
    running = True
    
    
    # RUN SCRAPING LOOPER
    while times_to_update > 0 :
        delta_time, last_time = CalculateTime(last_time)
        handler, time_left, times_to_update, update_time, delta_time = LoopScraper(handler, time_left, times_to_update, update_time, delta_time)
    


def StraightBetMain():
    
    # Create Stikerdot Handler
    handler = CreateHandler()
    handler.add_action(ScrapeLeaguesAndGamesStraight)
    
    time.sleep(10) 
    raw_data = handler.actions["ScrapeLeaguesAndGamesStraight"].invoke()
    
    # Process raw data into model
    games = CreateBasicModelsFromStraightRawData_Stikerdot(raw_data)
    
    for game in games:
        print (game)
    
    

if __name__ == '__main__':
    #LiveBetMain()
    StraightBetMain()