import requests


"""
Štěpán's program to get stats from ed forum
"""

def play():
    username = str(input("Please enter your Edsterm username >"))
    password = str(input("Please enter your Edsterm password\nYour password doesn't persist after exiting program >"))

    url1 = 'https://us.edstem.org/api/login_type'
    post1 = {"login":"ics2020-010@fit.cvut.cz"}
    url2 = 'https://us.edstem.org/api/token'
    post2 = {"login":"ics2020-010@fit.cvut.cz","password":""}

    with requests.session() as s:
        r = s.post(url1, json=post1)
        r = s.post(url2, json=post2)









if __name__ == '__main__':
    play()