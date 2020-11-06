import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(driver, username, password):
    
    # Get the username field by using the elements name property
    e_username = driver.find_element_by_name("customerID")
    e_password = driver.find_element_by_name("Password")
    
    e_form = driver.find_element_by_name("client login")
    
    e_username.send_keys("R1036")
    e_password.send_keys("yeet3")
    # Locate the login button. Im sure theres an easier way.
    # https://stackoverflow.com/questions/24795198/get-all-child-elements
    all_children_by_xpath = e_form.find_elements_by_xpath(".//*")
    
    e_login_btn = None
    for c in all_children_by_xpath:
        if (c.text.lower() == 'login'):
            if (c.tag_name == 'button'):
                e_login_btn = c
    
    # Give the browser time to load the form completely before we submit data        
    time.sleep(1.5)

    e_login_btn.click() # not working using send)keys(keys.RETURN)
    #e_login_btn.send_keys(Keys.RETURN)
    return driver


    


# create a new Firefox session
#driver.implicitly_wait(30)
#driver.maximize_window()

## Define username and password for login 
username = "R1036"
password = "yeet3"

## Crete Driver
driver = webdriver.Firefox()

## Navigate to the application home page
driver.get("http://www.strikerdot.com")

driver = login(driver, username, password)
time.sleep(1.5)

# After login sometimes we get a Frame of announcements. Clicking anywhere will disable this frame.
# driver.click() # UNTESTED!

# Go to live betting section
driver.get("https://www.strikerdot.com/sports.html?livebettingEZ=ready?logged=1#!")
time.sleep(3)

# Navigate to football
# Get the sports listing container
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "myDynamicElement"))
    )
    print(element)
finally:
    pass

e_sports = driver.find_element_by_class_name("sports-list")
print (e_sports)

# Scrape football section
# - Locate Wanted html elements
# - Read wanted elements for the wanted data
# - Store that wanted data in a basic way

## close the browser window
#driver.quit()

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
