
import pprint
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver, username, password, clickTime=3):
    
    # Get the username field by using the elements name property
    e_username = driver.find_element_by_name("customerID")
    e_password = driver.find_element_by_name("Password")
    
    e_form = driver.find_element_by_name("client login")
    
    e_username.send_keys(username)
    e_password.send_keys(password)
    
    # Locate the login button. Im sure theres an easier way.
    # https://stackoverflow.com/questions/24795198/get-all-child-elements
    all_children_by_xpath = e_form.find_elements_by_xpath(".//*")
    
    e_login_btn = None
    for c in all_children_by_xpath:
        if (c.text.lower() == 'login'):
            if (c.tag_name == 'button'):
                e_login_btn = c
    
    # Give the browser time to load the form completely before we submit data        
    time.sleep(clickTime)

    e_login_btn.click() # not working using send)keys(keys.RETURN)
    #e_login_btn.send_keys(Keys.RETURN)
    return driver




def isEqual(elem, _type):
    return elem == _type

def isLeague(elem):
    return isEqual(li.get_attribute('class'), 'league')

def isGame(elem):
    return isEqual(li.get_attribute('class'), 'game')
    
def GetLeagueText(elem):
    league = li.find_element_by_xpath(".//div").text
    return league
    
def GetGameData(elem):
    data = []
    
    for elem in li.find_elements_by_xpath(".//*"):
        
        elem_class = elem.get_attribute('class')
        
        if (isEqual(elem_class, 'game-team')):
            data += [elem.text]
        
        elif (isEqual(elem_class, "game-detail")):
            div = elem.find_element_by_xpath('.//div')
            data += [elem.text]
    return data


# Go to live betting section
driver.get("https://www.strikerdot.com/sports.html?livebettingEZ=ready?logged=1#!")

time.sleep(15)

# Navigate to football
# Get the sports listing container

# Scrape football section
# - Locate Wanted html elements
# - Read wanted elements for the wanted data
# - Store that wanted data in a basic way

#frames = driver.find_elements_by_xpath('//frame')
#print (frames)
#driver.switch_to.frame(frame)

# getLiveFootball element   icon-sportAmericanFootball sport-title

sections = driver.find_elements_by_xpath("//section")
section = sections[-1]
frame = section.find_elements_by_xpath("//iframe")[0]

driver.switch_to.frame(frame)

e_football = driver.find_element_by_xpath ("//a[@class='icon-sportAmericanFootball sport-title']")
#e_football_spans = e_football.find_element_by_xpath("//span")

print(e_football)

# Get straight to the game list container
ul = e_football.find_element_by_xpath("..//following-sibling::li//div//div//ul")
lis = ul.find_elements_by_xpath('.//li')


## In order: Game 1 and 2 should be Team1 vs Team2
# League 1(College): {"Game 1": {"Team 1": score1, "Team 2": score2}, "Game 2": {...} },
# League 2(NFL)    : {"Game 1": {"Team":score, "Team:score}, "Game 2": {...} }

data = {}
league = ""

for li in lis:
    # Sort data by leagues, NFL, 
    if (isLeague(li)):
        league = GetLeagueText(li)
        data[league] = [] # Create a list
        
    # Scrape game and store in current league
    elif (isGame(li)):
        game_data = GetGameData(li)
        data[league] += [game_data]


pprint.pprint(data)
       


#for span in e_football_spans:
#    print(span.text)

# one li down past american football is next live game

# Organize data
# - implement pandas

# Store data in a database

# Show data
# - implement matplotlib

# Allow manipulation of data
# - Some form of GUI

# Begin to sort data in intresting ways.

# Begin to calculate winning odds of bets
# Store process of determining winning odds and those results

# Determine propbablity of the aboves speculations on winning bets

# Types of bets.
# Basic Odds: If probablity of winning is within a certain percent take the bet

# Potential Gains: Take the odds of winning, potential gains and cost of a bet and if above a certain percent, margin and cost, take the bet.

# Betting Cluster: A group of bets

# Swarm Betting: Apply the Potential Gains bet to a cluster of bets. 
# Meaning take a number of bets, if the overall winnings, cost, and percent of winning are within certain constraints take the bet.
