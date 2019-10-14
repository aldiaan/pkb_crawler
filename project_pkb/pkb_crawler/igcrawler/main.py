
from igcrawler_core.scrapper import Scrapper
from igcrawler_core.auth import login

def start(args):
    
    igcrawler = Scrapper()
    savetodb = args.save_db
    logged_in = False

    if args.username != None and args.password != None:
        cookies = login(args.username, args.password)
        for cookie in cookies:
            igcrawler.add_cookies(cookie)
        logged_in = True
            
    if args.c:                        
        igcrawler.level1(args.uid, None, 1, logged_in=logged_in, _continue=True, savetodb=savetodb)

    if args.uid != None:        
        igcrawler.level1(args.uid, args.limit, int(args.ring), logged_in=logged_in, _continue=False, savetodb=savetodb)                    

    
