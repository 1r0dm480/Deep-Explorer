# -------------------- IMPORTS --------------------
try:
    from time import sleep
except ImportError:
    print("Error importing 'sleep', from 'time'")
    exit()

try:
    from interruptingcow import timeout
except ImportError:
    print("Error importing 'interruptingcow'")
    exit()
try:
    import sys
except ImportError:
    print("Error importing 'sys'")
    exit()
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error importing 'beatifulsoup'")
    exit()
try:
    import requests
except ImportError:
    print("Error importing 'requests' module")
    exit()
try:
    import os
except ImportError:
    print("Error importing 'os' module")
    exit()
    
# -------------------- PROXIES --------------------

proxies = {'http':'socks5h://127.0.0.1:9050', 'https':'socks5h://127.0.0.1:9050'} # tor proxy

# -------------------- FUNCS --------------------

def crawl(option, deeplinks, link):
    if option is "default":
        length_of_web_links_to_crawl = len(deeplinks)
        iterations = 0
        
        while len(deeplinks) <= number_results or length_of_web_links_to_crawl <= iterations:
            with timeout(10):
                crawl = requests.get(deeplinks[iterations], proxies=proxies)
            crawl = crawl.text
            try:
                soup = BeautifulSoup(crawl, "lxml")
            except:
                print("Error creating 'soup' object")
                os.system("sudo service tor stop")
                exit()
            
            for a in soup.find_all('a', href=True):
                if len(deeplinks) >= number_results:
                    print(" \033[0;32m LINKS COLLECTED!\033[0m")
                    os.system("sudo service tor stop")
                    exit()
                darklink = isonion(iterations['href'])    
                if darklink:
                # write to file
                    if not darklink in deeplinks:
                        with open("results.txt", 'a') as f:
                            f.write("\n" + darklink)
                        f.close()
                        deeplinks.append(darklink)         
                        print(darklink)    
            iterations+=1          
    if option is "all":
        with timeout(10):
            crawl = requests.get(link, proxies=proxies)
        crawl = crawl.text
        try:
            soup = BeautifulSoup(crawl, "lxml")
        except:
            print("Error creating 'soup' object")
            os.system("sudo service tor stop")
            exit()
        print("Crawling from : " + "[\033[0;31m" + link + "\033[0m]")
        for a in soup.find_all('a', href=True):
            if len(deeplinks) >= number_results:     
                print(" \033[0;32m LINKS COLLECTED!\033[0m")
                os.system("sudo service tor stop")
                exit()
                
            darklink = isonion(a['href'])   
            if darklink:
                # write to file
                if not darklink in deeplinks:
                    with open("results.txt", 'a') as f:
                        f.write("\n" + darklink)
                    f.close()
                    deeplinks.append(darklink)
                    print(darklink)

def isonion(darklink):
    if not ".onion" in darklink or "http://msydqstlz2kzerdg.onion" in darklink: # if there's not ".onion" in href, its not a tor link so... return False
        return False
        
    if "http://" in darklink: # if we are here, the link contains a .onion so, lets 'clean' it
        isvalid = darklink.split("http://")[1].split(".onion")[0]
        isvalid = "http://" + isvalid + ".onion"
        try:
            with timeout(10):
                maybevalid = requests.get(isvalid, proxies=proxies) # can we connect to it?
        except:
            return False
        if maybevalid.status_code is not 200:
            return False # if not... return False
        else:
                return isvalid # else... return the link!
                
def search(crawling):
    darklinks = []
    print("Searching. . . ", end="", flush=True)
    web = "http://msydqstlz2kzerdg.onion/search/?q="
    search_query = web + search_string
    
    try:
        content = requests.get(search_query, proxies=proxies)
        content = content.text
    except:
        print("\nError connecting to server")  
        exit()
    try:
        soup = BeautifulSoup(content, "lxml")
    except:
        print("\nError creating 'soup' object")
        os.system("sudo service tor stop")
        exit()
    print(" \033[0;32m [OK]\033[0m")
    print("Checking links ")
    for a in soup.find_all('a', href=True): # for each href in browser response
        if len(darklinks) >= number_results: # if reached number of links
            print(len(darklinks))
            print("SEARCH COMPLETE" +  "\033[0;32m [OK]\033[0m")
            os.system("sudo service tor stop")
            exit()
            
        darklink = isonion(a['href']) # if not reached, darklink will be a tor link ( if current href is valid)
        if darklink: # if valid...  
            if not darklink in darklinks: # if not present in list
                with open("results.txt", 'a') as f:
                    f.write("\n" + darklink)
                f.close()
                print(darklink)   
                darklinks.append(darklink) # add it
                if "all" in crawling:
                    crawl("all", darklinks, darklink)
    if "none" in crawling:
        print("Search completed.")
        exit()
    print("Not enought links in browser, crawling...")
    if darklinks:
        if "default" in crawling:
            crawl("default", darklinks)
        else:
            print("Not enought links in browser, but crawl disabled")
            os.system("sudo service tor stop")
            exit()
    else:
        print("0 links!, cant crawl...")
        os.system("sudo service tor stop")
        exit()    

def torproxy():
    print("Checking Tor instance", end="", flush=True)
    try:
        check = requests.get("https://google.es", proxies=proxies)
    except:
        print(" [\033[0;31mNo connected\033[0m]")
        print("Starting Tor instance ", end="", flush=True)
        os.system("service tor start")
        sleep(8)
    print(" \033[0;32m [OK]\033[0m")
    print("Checking Tor proxy ", end="", flush=True)
    try:
        check = requests.get("https://google.es", proxies=proxies)
    except:
        print(" => [\033[0;31mERROR\033[0m] proxy is refusing connections")
        os.system("sudo service tor stop")
        exit()
    print(" \033[0;32m [OK]\033[0m")

# -------------------- MAIN PROGRAM --------------------    
    
def printred(banners):
    def interns():
        print("\033[0;31m")
        banners()
        print("\033[0m")
    return interns
    
@printred
def banner():
    print("     __                                         __                       ")
    print(" .--|  .-----.-----.-----.   .-----.--.--.-----|  .-----.----.-----.----.")
    print(" |  _  |  -__|  -__|  _  |   |  -__|_   _|  _  |  |  _  |   _|  -__|   _|")
    print(" |_____|_____|_____|   __|   |_____|__.__|   __|__|_____|__| |_____|__|  ")
    print("                   |__|                  |__|                            ")
    print("                                                                         ")
    print("                                                                         ")
    print("                                                                         ")

banner()
if len(sys.argv) is not 4 or sys.argv[3] not in ["all", "none", "default"]:
    print("dexplorer.py SEARCH NUMBER_OF_RESULTS crawl_options")
    print("Crawl Options:")
    print("             all) crawl each link")
    print("             none) dont crawl")
    print("             default) crawl if not enough links")

    exit()

    
if __name__ == "__main__":
    try:    
        torproxy() # set up tor proxy
        search_string = sys.argv[1]
        number_results = int(sys.argv[2])
        crawld = sys.argv[3]
        search(crawld) # main func
    except KeyboardInterrupt:
        print("\nExiting. . .")
        os.system("sudo service tor stop")
    
