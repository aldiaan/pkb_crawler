import os
import json
import random

from time import sleep
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from igcrawler_common.const import BASE_URL, FOLLOWERS_LIMIT
from igcrawler_common.selector import *

from igcrawler_core.helpers import *
from igcrawler_core.database import Database

class Scrapper:
    def __init__(self):
        options = Options()
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)

    def wait_for_elements(self, elements, time):
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, elements)))                       

    def wait_for_element(self, element, time):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located((By.CSS_SELECTOR, element)))                               

    def add_cookies(self, cookies):
        self.driver.get(BASE_URL)
        self.driver.add_cookie(cookies)

    def level1(self, uid, limit, ring=1, logged_in=False, _continue = False, savetodb=False): 

        if savetodb:
            db = Database()

        if limit == None:
            limit = 999999999999999
        
        c = {
            'path' : '',
            'uids' : [],
            'last_idx' : 0
        }
        
        once = True

        if(not _continue):   
            if os.name != 'nt':         
                # linux (posix)
                path = (os.path.dirname(os.path.realpath(__file__))).replace('/igcrawler_core', '/data/') + datetime.now().strftime("%d_%m_%Y_%H%M%S") + '_level1_' + 'dump.csv'       
            else:
                # windows (nt)
                path = (os.path.dirname(os.path.realpath(__file__))).replace('\\igcrawler_core', '\\data\\') + datetime.now().strftime("%d_%m_%Y_%H%M%S") + '_level1_' + 'dump.csv'                
            if not savetodb:
                open(path, 'w+')
            uids = self.get_user_followers(uid, ring)                
            c['path'] = path
            c['uids'] = uids
            write_mode = 'w'
        else:            
            print('continuing from last scrapping ... ')
            write_mode = 'a'
            with open('continue.json') as json_file:                
                data = json.load(json_file)
                path = data['path']
                c['path'] = path
                uids = data['uids']
                uids = uids[data['last_idx']:]    
                c['uids'] = uids                
            
        try:
            datas = []
            for count_id, uid in enumerate(uids):
                self.driver.get(BASE_URL + uid)        
                print('user number : {}'.format(str(count_id + 1)))
                c['last_idx'] = count_id + 1
                i = 0            
                try:
                    self.wait_for_element(PRIVATE_PAGE, 3)
                    continue
                except:                
                    if (logged_in == False and once):
                        self.wait_for_element(LOGIN_PROMPT_CLOSE, 3).click()
                        once = False 

                    try:                   
                        self.wait_for_element(POST_LOCATION, 3).click()

                        while i < int(limit):                            
                            print('fetching post number {} from {} ... '.format(i + 1, uid))
                            try:
                                self.wait_for_element(POST_DATE, 3.5)                    
                                post_content = ''
                                comment = ''

                                try:
                                    
                                    try:
                                        posts = self.driver.find_elements_by_css_selector(POST_CONTENT)                        
                                        post_content = posts[0].text
                                        word_tags = tags_counter(post_content)                                        
                                        if len(posts) > 1:
                                            comment = posts[1].text
                                    except:
                                        pass
                            
                                    try:
                                        likes_watch = self.driver.find_element_by_css_selector(POST_LIKES).text
                                    except:
                                        try:
                                            n = self.driver.find_element_by_css_selector(POST_WATCH_COUNT)
                                            n.click()                                            
                                            likes_watch = self.wait_for_element(POST_VIDEO_LIKE, 0.5).text
                                            self.driver.execute_script("clk = document.querySelector('{}');clk.click();console.log(clk)".format(POST_WATCH_COUNT))                                            
                                        except:                                            
                                            try:
                                                likes_watch = self.driver.find_element_by_css_selector(POST_LIKE).text
                                            except:
                                                pass

                                    if likes_watch == '1 like':
                                        likes_watch = '1'
                                    elif likes_watch == 'like this':
                                        likes_watch = '0'                

                                    data = {
                                        'account' : uid,
                                        'content' : remove_tags(post_content),
                                        'tags' : word_tags,
                                        'likes' : likes_watch,
                                        'comment' : comment
                                    }   

                                    if not savetodb:
                                        datas.append(data)                                                            
                                    else:
                                        print(data)
                                        db.lvl1.insert_one(data)
                                    print(json.dumps(data, indent=4, sort_keys=True))

                                except:
                                    # no content (maybe?)
                                    pass
                            except:
                                # long post loading
                                pass

                            finally:
                                try:
                                    sleep(random.uniform(0, 0.5))
                                    self.driver.find_element_by_css_selector(POST_NEXT_BUTTON).click()
                                    i += 1
                                except:
                                    # break if no next button found                        
                                    i = int(limit)
                    except:                                            
                        i = int(limit)
            if not savetodb:
                save_to_csv(path, datas, write_mode)    
                print('saved to -> {} ({})'.format(path, convert_bytes((os.stat(path)).st_size)))            
        except KeyboardInterrupt:
            print('ended with keyboard interrupt')
            if not savetodb:
                save_to_csv(path, datas, write_mode) 
                print('saved to -> {} ({})'.format(path, convert_bytes((os.stat(path)).st_size)))                        
    
        except:
            print('ended with error:')            
            if not savetodb:
                save_to_csv(path, datas, write_mode)    
                print('saved to -> {} ({})'.format(path, convert_bytes((os.stat(path)).st_size)))
            
        finally:                                        
            with open('continue.json', 'w') as fp:
                json.dump(c, fp)            

    
    def get_user_followers(self, uid, ring=1):

        def get_followers(followers, start_idx, i):
            print(followers)
            print('ring --> {} followers --> {}'.format(i, str(len(followers))))
                  
            if i == ring:                             
                return followers 

            sidx = len(followers)
            # print(start_idx)
            for idx in range(start_idx, len(followers)):
                # print(followers[idx])
                self.driver.get(BASE_URL + followers[idx])
                try:
                    private = self.wait_for_element(PRIVATE_PAGE, 3)
                    print('private page skipping ...')
                except:
                    try:
                        el_followers = self.wait_for_elements(USER_FOLLOWER, 0)[0]
                        el_followers.click()
                    except:
                        return followers
                    sleep(2)
                    followers_count = el_followers.get_attribute('title')
                    followers_count = followers_count.replace(',', '')

                    uids = []
                    if followers_count == '':
                        followers_count = '0'
                    if int(followers_count) > FOLLOWERS_LIMIT:
                        followers_count = FOLLOWERS_LIMIT

                    while len(uids) < int(followers_count):                             
                        self.driver.execute_script("x1 = document.querySelector('div.isgrP');x1.scrollBy(0,x1.offsetHeight - 70)")
                        sleep(0.4)
                        uids = self.driver.find_elements_by_css_selector(FOLLOWER_UID)
                        if len(uids) < 12:
                            break
                        
                        # print(str(len(uids)) + '/' + str(followers_count))

                    for uid in uids:
                        if uid.get_attribute('title') not in followers:
                            followers.append(uid.get_attribute('title'))
                    # print(followers)
            
            i += 1                  
            return get_followers(followers, sidx, i)
        
        return get_followers([uid], 0, 1)

        
    
        
