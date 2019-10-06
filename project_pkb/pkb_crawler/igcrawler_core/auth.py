import requests

from igcrawler_common.const import BASE_URL, UA_DESKTOP, LOGIN_API

def login(username, password):
    session = requests.session()
    csrf_token = session.get(BASE_URL, verify=False).cookies['csrftoken']

    data = {
        'username' : username,
        'password' : password
    }

    headers = {
        'Referer' : BASE_URL,
        'X-CSRFToken' : csrf_token,
        'User-Agent' : UA_DESKTOP
    }
        
    do_login = session.post(LOGIN_API, data=data, headers=headers, allow_redirects=True)
    cookies = []

    for cookie in do_login.cookies:    
        cookies.append({
            'name' : cookie.name,
            'value' : cookie.value,
            'domain' : cookie.domain,
            'path' : cookie.path
        })    
        
    return cookies