import requests


"""
Štěpán's program to get stats from ed forum
"""


def play():

    # username = str(input("Please enter your Edsterm username > "))
    # password = str(input("Please enter your Edsterm password\nYour password doesn't persist after exiting program > "))

    api_urls = {'login':'https://us.edstem.org/api/token',
                'new_thread':'https://us.edstem.org/api/courses/2014/threads',
                }
    login_post = {"login": "ics2020-010@fit.cvut.cz","password": ""}
    target_payload = {"comment":{"content":"<document version=\"2.0\"><paragraph>Spaaaaaaaaaaaaaaaaaaaaaam</paragraph></document>","is_private":False,"is_anonymous":False}}
    headers = {}

    with requests.session() as s:
        r = s.post(api_urls['login'], json=login_post) # login api, returns unique token
        while r.status_code >= 300: # Checks for correct credentials
            print('username or password is not correct, please reenter correct credentials')
            # username = str(input("Please reenter your username > "))
            # password = str(input("Please reenter your password > "))
            r = s.post(api_urls['login'], json=login_post)
        token_setup = r.text.split('"')
        headers["x-token"] = token_setup[3] # saves token with x-token key
        print(headers)
        #r = s.post(target_url, json=target_payload, headers=headers, cookies=cookies)
        #print(r.text)

def post_new_thread(s, headers):
    type_list = {'p': '"post"', 'q': '"question"'}
    category_list = {'general': '"General"', 'schedule': '"Schedule"', 'logistics': '"Logistics"',
                     'assignments': '"Assignments"', 'code': '"Code"', 'social': '"Social"', 'sections': '"Sections"'}
    subcategory_days = ['"Day 1"', '"Day 2"', '"Day 3"', '"Day 4"', '"Day 5"', '"Day 6"', '"Day 7"', '"Day 8"', '"Day 9"',
                        '"Day 10"', '"Day 11"', '"Day 12"', '"Day 13"', '"Day 14"']
    subcategory_program = {'karel':'"Karel"', 'python':'"Python"'}
    subcategory = '""'



    print("You chose to post a new thread. If you want to exit, enter anytime -1")
    title = str(input("Choose name of your thread: "))
    if title == "-1":
        return 0
    post_type = str(input("Choose type of post - enter 'p' for post and 'q' for question"))
    while type != "q" or type != "p":
        if type == "-1":
            return 0
        post_type = str(input("You entered wrong type, enter only 'p' for post, 'q' for question and '-1' to go back: "))
    print("Possible categories are\n", category_list.keys())
    category = str(input("Choose one of available categories for your post: "))
    checked_number = 0
    while checked_number == 0:
        for check in category_list:
            if check == category:
                checked_number = 1
                if category == 'code':
                    subcategory = subcategory_program[str(input('Please choose "python" or "karel" as your subcategory'))]
                elif category == 'sections':
                    subcategory = subcategory_days[int(input("Please enter number of the day when your problem occurred")) - 1]
            if category == "-1":
                return 0
        print("You chose unlisted category, try it again")
        category = str(input("Choose one of the listed categories: "))
    text = str(input("Input your message: "))

    payload = {"thread":{"type":"post","title":"Ed api test - post, private-false, anonymous=false, category=General","category":"General","subcategory":"","subsubcategory":"","content":"<document version=\"2.0\"><paragraph>test paragraf text</paragraph></document>","is_pinned":false,"is_private":false,"is_anonymous":false,"anonymous_comments":false}}

if __name__ == '__main__':
    play()