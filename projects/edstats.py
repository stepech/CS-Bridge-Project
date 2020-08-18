import requests


"""
Štěpán's program to get stats from ed forum
"""


def play():
    #username = str(input("Please enter your Edsterm username >"))
    #password = str(input("Please enter your Edsterm password\nYour password doesn't persist after exiting program >"))

    url1 = 'https://us.edstem.org/api/login_type'
    post1 = {"login": "ics2020-010@fit.cvut.cz"}
    url2 = 'https://us.edstem.org/api/token'
    post2 = {"login": "ics2020-010@fit.cvut.cz","password": ""}
    target_url = 'https://us.edstem.org/api/threads/108601/comments'
    target_payload = {"comment":{"content":"<document version=\"2.0\"><paragraph>Second attemp with remote post bot, on private thread. Test.</paragraph></document>","is_private":False,"is_anonymous":False}}

    with requests.session() as s:
        r = s.post(url1, json=post1)
        r = s.post(url2, json=post2)
        cookies = r.cookies
        headers = {}
        token_setup = r.text.split('"')
        headers["x-token"] = token_setup[3]
        print(headers)
        r = s.post(target_url, json=target_payload, headers=headers, cookies=cookies)
        print(r.text)











if __name__ == '__main__':
    play()