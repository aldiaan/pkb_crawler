
from igcrawler_core.scrapper import Scrapper
from igcrawler_core.auth import login

def start(args):
    
    if args.mode != None:
        igcrawler = Scrapper()
        logged_in = False

        if args.username != None and args.password != None:
            cookies = login(args.username, args.password)
            for cookie in cookies:
                igcrawler.add_cookies(cookie)
            logged_in = True
                
        if args.c and args.mode == '1':                        
            igcrawler.level1(args.uid, None, 1, logged_in=logged_in, _continue=True)

        if args.uid != None:
            if (args.mode == 'level1' or args.mode == '1'):                
                igcrawler.level1(args.uid, args.limit, int(args.ring), logged_in=logged_in, _continue=False)
            elif (args.mode == 'level2' or args.mode == '2'):
                igcrawler.level2(args.uid, args.limit, int(args.ring), logged_in=logged_in)
        

       
    else:
        print('no mode selected')
    

    