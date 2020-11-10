import time


from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions



def isEqual(elem, _type):
    return elem == _type


def WaitForElement(handler, xpath, timeout=7):
    
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)        
    
    element = WebDriverWait(handler, timeout, ignored_exceptions=ignored_exceptions)\
        .until(expected_conditions.presence_of_element_located((By.XPATH, xpath))) 




# An action is every change and event that happens in a process. 
class Action(object):
    def __init__(self, name="Action", handler=None):
        self.name = name
        self.handler = handler
        
    # Does nothing
    def invoke(self): pass

    def FromHandler_FindIFrame(self):
        return self.handler.driver.find_elements_by_xpath("//iframe")[0]
    
    def FromHandler_FindElement(self, xpath): 
        return self.handler.driver.find_element_by_xpath(xpath)
        
    def FromHandler_FindElements(self, xpath): 
        return self.handler.driver.find_elements_by_xpath(xpath)
    
    def FromHandler_FindElementAttribute(self, xpath, attribute):
        return self.FromHandler_FindElement(xpath).get_attribute(attribute)
        
        
    # Abstract method, given a function and its parameters call it inside of a try excpet block, return the results
    def TRY(self, func, verbose=True, *args, **kwargs):
        if (verbose): print("[!] -- TRY - %s()" % (func.__name__), ', '.join(args))
        results = None        
        try:
            results = func(*args, **kwargs)
            if (verbose): print(results)            
        except Exception as e: 
            if (verbose): print ('error', e)
            return None
        return results
        
    # Same concept as the TRY() method but loops over a number of times upon errors and returns results immeditaley if successful.
    def TRY_LOOP(self, func, times=3, verbose=True, *args, **kwargs):
        results = None
        while (times > 0):    
            if (verbose): print("[!] -- TRY_LOOP %d - %s()" % (times, func.__name__), ', '.join(args))
            try:
                times = 0
                results = func(*args, **kwargs)    
     
            except Exception as e: 
                times -= 1
                if (verbose): print ('error', e)
        return results

        
    def TRY_FINDING_ELEMENT(self, path, verbose=True):
        return self.TRY(self.FromHandler_FindElement, verbose, path)

    def TRY_FINDING_ELEMENT_LOOP(self, path, times=3, verbose=True):
        return self.TRY_LOOP(self.FromHandler_FindElement, times, verbose, path)

    def TRY_FINDING_ELEMENT_ATTRIBUTE(self, path, attribute, verbose=True):
        return self.TRY(self.FromHandler_FindElementAttribute, verbose, path, attribute)
    

        
    def TRY_FINDING_ELEMENTS(self, path, verbose=True):
        return self.TRY(self.FromHandler_FindElements, verbose, path)

    def TRY_FINDING_ELEMENTS_LOOP(self, path, times=3, verbose=True):
        return self.TRY_LOOP(self.FromHandler_FindElements, times, verbose, path)

    
    
    



class Login(Action):
    def __init__(self, handler):
        super(Login, self).__init__('Login', handler)
        
    # Login and try a number of times of unsuccessful
    def invoke(self, tries=3, post_login_redirect=True):
        print("handler login action, post_login_redirect= " + str(post_login_redirect))
        return self.TRY_LOOP(self.Login, tries, True, post_login_redirect = post_login_redirect)

    def Login(self, post_login_redirect = True):
        self.Navigate()
        self.FillLoginForm()
        self.ClickLogin()
        if post_login_redirect:
            self.PostLoginRedirect()
        return True
        
    def Navigate(self):
        self.handler.get(self.handler.url_login)
        
    # Get the username field by using the elements name property
    def FillLoginForm(self):
        e_username = self.handler.driver.find_element_by_name("customerID")
        e_password = self.handler.driver.find_element_by_name("Password")
        
        e_username.send_keys(self.handler.username)
        e_password.send_keys(self.handler.password)
        
    def ClickLogin(self):
        e_login_btn = None
        e_form = self.handler.driver.find_element_by_name("client login")
        all_children_by_xpath = e_form.find_elements_by_xpath(".//*")
        for c in all_children_by_xpath:
            if (c.text.lower() == 'login'):
                if (c.tag_name == 'button'):
                    e_login_btn = c
        
        e_login_btn.click()
        time.sleep(self.handler.nav_time)
        return
   
    def PostLoginRedirect(self):
        self.handler.get(self.handler.url_post_login)
        time.sleep(self.handler.nav_time)        
            
     
    
      



# Scrape League and Game Data .
# This does not include bets
class ScrapeLeaguesAndGames(Action):
    
    def __init__(self, handler):
        super(ScrapeLeaguesAndGames, self).__init__('ScrapeLeaguesAndGames', handler)
        self.SetAbsPaths()
        self.data = {}
    
    #def FromHandler_FindIFrame(self):
        #return self.handler.driver.find_elements_by_xpath("//iframe[@id='live']")
        
    
    ### RUN / START
    def invoke(self, timeout=10):
        
        self.handler.driver.switch_to.default_content();

        # Find Frame, Go inside
        print("[+][!] Finding Frame...")
        frame = self.TRY_FINDING_ELEMENT_LOOP("//iframe[@id='live']")
        self.handler.driver.switch_to.frame(frame)
        #self.TRY_LOOP(self.handler.driver.switch_to.frame, 3, True, "live")
        print("[+] Frame Found\n")
        
        ### Not working right now
        #game_count = self.GetGameCount()
        #print ("[**] No Games are on.")
        #if (game_count == 0): return self.data
        ###
        
        # Get Data and return it
        self.GetLeagueAndGames()
        return self.data
    ###    
    
    
    ### SETUPS
    def SetAbsPaths(self):
        # Set absoulte paths to elements 
        self.e_football_xpath = "//a[@class='icon-sportAmericanFootball sport-title']"
        self.e_football_list_xpath = "//ul[@id='s12']/li"
        self.e_baseball_list_xpath = "//ul[@id='s16']/li"
        self.e_basketball_list_xpath = "//ul[@id='s18']/li"
        
    ###
    
    ### VALIDATIONS
    def isLeague(self, elem):
        return isEqual(elem.get_attribute('class'), 'league')
    
    def isGame(self, elem):
        return isEqual(elem.get_attribute('class'), 'game')
    ###    
    
 
 
    ### CORE ACTION CODE
    
    def GetGameCount(self):
        count = self.TRY_FINDING_ELEMENT("//span[@id='fooCount']").text
        if (count in ["", None]): count = 0
        else: count = int(count)
        return count


    # Previous Requirement: Navigate inside the IFRAME. 
    # Return a dictionary of the leagues and games
    def GetLeagueAndGames(self, times=3):
        
        while (times > 0):
            print ("[+] GettingLeagueAndGames() - %d" % (times))  
            times -= 1;
            self.data = {}
            league = "" 
            
            try:
                
                #elems = self.TRY_FINDING_ELEMENTS(self.e_football_list_xpath)
                elems = self.TRY_FINDING_ELEMENTS(self.e_baseball_list_xpath) 
                #elems = self.TRY_FINDING_ELEMENTS(self.e_basketball_list_xpath) 
                
                print ("[+] Found %d Elements " % (len(elems)))
                self.__GetLeagueAndGames(elems)
                
                #def TRY_LOOP(self, func, times=3, verbose=True, *args, **kwargs):
                #self.TRY_LOOP(self.__GetLeagueAndGames, 3, True, elems=elems)

                # If we succedded in getting all the data exit the while loop
                times = 0 # While Loop Conditoin
                
            # If we receieve a stale element error we know that the web site just updated
            except StaleElementReferenceException as e: print("Stale Element Error")
            except Exception as e: print ("Error", e)
                
            print()
        
        return self.data
        


    # Actual Code that will get us our data
    def __GetLeagueAndGames(self, elems):
        print("\n__GetLeagueAndGames()")        
        league = ""
        for el in elems:
            print (); print (el)
            
            # This element is a league, The following will be games, until a new League appears
            if (self.isLeague(el)): 
                print ("[+][+] IsLeague")
                league = self.AddLeague(el)
                print (str(league))

            # Scrape game and store in current league
            elif (self.isGame(el)): 
                game = self.AddGame(league, el)
                print(str(game))       

            print ("[+][+] SUCCESS")            

        
    # Add a league to the data set.
    def AddLeague(self, elem):
        league = self.GetLeagueText(elem)
        self.data[league] = [] # Create a list
        return league
    
    # Add a game to a league in the data set
    def AddGame(self, league, elem):        
        game_data = self.TRY_LOOP (self.GetGameData, times=3, verbose=True, element=elem)
        self.data[league] += [game_data]
        return game_data
    ### 
        
        
    ### EXTRATIONS
    def GetLeagueText(self, elem, timeout=7):
        print ("[+] Getting League Data")       
        return elem.find_element_by_xpath(".//div").text
        
        
    def GetGameData(self, element):
        print ("[+] Getting Game Data")        
        # list that holds data in this order, both are strings that need parsing: 
        # data = [teams, game-data]        
        data = [] 
        
        # Get Every element in the in the game-details div.
        # Each element has a unique bit of data.
        elems = element.find_elements_by_xpath(".//*")
        for e in elems:
        
            
            # To determine what element/data we currently have lets gets its class name for some information
            e_class = e.get_attribute('class')
            
            # If the class of the element is 'game-team' we know we are accessing the teams playing in this game
            if (isEqual(e_class, 'game-team')):
                data += [e.text]
            
            # Else if the class of the element is 'game-detail' we know  there data like score and time. 
            elif (isEqual(e_class, "game-detail")):
                div = e.find_element_by_xpath('.//div')
                data += [e.text]
       
        # return the retrieved data
        return data
    
class ClickGames(Action):
    def __init__(self, game):
        super(ClickGame, self).__init__('ClickGame', handler)
        
    
    def invoke(self):
        handler.click()
        




class ScrapeLeaguesAndGamesStraight(Action):
    def __init__(self): pass
    
    def invoke(self): pass
