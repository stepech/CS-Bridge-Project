import requests
import re
from getpass import getpass

"""
Štěpán's program to get stats from ed forum
"""

def play():

    username = str(input("Please enter your Edsterm username > "))
    password = str(input("Please enter your Edsterm password > "))

    api_urls = {'login': 'https://us.edstem.org/api/token',
                'new_thread': 'https://us.edstem.org/api/courses/968/threads',
                'delete_thread': 'https://us.edstem.org/api/threads/'
                }
    login_post = {"login": username, "password": password}
    headers = {}

    with requests.session() as s:
        r = s.post(api_urls['login'], json=login_post)  # login api, returns unique token
        while r.status_code >= 300:  # Checks for correct credentials
            print('username or password is not correct, please reenter correct credentials and check your internet connection')
            username = str(input("Please reenter your username > "))
            password = str(input("Please reenter your password > "))
            login_post = {"login": username, "password": password}
            r = s.post(api_urls['login'], json=login_post)
        del password

        for i in range(20):
            print()
        print("Successfully signed in")
        token_setup = r.text.split('"')
        headers["x-token"] = token_setup[3]  # saves token with x-token key
        x = 1
        while x != 0:
            print("Would you like to")
            print("1 - Read the forum")
            print("2 - Create new thread")
            print("3 - Delete my thread")
            print("0 - exit this program")
            x = int(input())
            if x == 1:
                s = read(s, headers)
            elif x == 2:
                payload = post_new_thread()
                r = s.post(api_urls['new_thread'], json=payload, headers=headers)
                if r.status_code < 300:
                    print("Message successfully sent")
                else:
                    print("There was some error sending your message")
            elif x == 3:
                threads, links = delete_thread(s, headers)
                y = int(input("Choose number of thread you'd like to delete or -1 to cancel "))
                if len(threads) == 0:
                    print("Sorry, you have no threads you can delete")
                elif 1 <= y <= (len(links)+1):
                    r = s.delete(api_urls['delete_thread']+str(links[y-1]), headers=headers)
                    if r.status_code < 300:
                        print("Your thread \""+threads[y-1]+'" was successfully deleted')
                    else:
                        print("There was some mistake during connection to server")




def post_new_thread():
    type_list = {'p': 'post', 'q': 'question'}
    category_list = {'general': "General", 'schedule': "Schedule", 'logistics': "Logistics",
                     'assignments': "Assignments", 'code': "Code", 'social': "Social", 'sections': "Sections"}
    subcategory_days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7", "Day 8", "Day 9",
                        "Day 10", "Day 11", "Day 12", "Day 13", "Day 14"]
    subcategory_program = {'karel': "Karel", 'python': "Python"}
    subcategory = ""
    is_private = False
    is_anonymous = False

    print("You chose to post a new thread. If you want to exit, enter anytime -1")
    title = str(input("Choose name of your thread: "))
    if title == "-1":
        return 0

    post_type = str(input("Choose type of post - enter 'p' for post and 'q' for question "))
    while post_type != "q" and post_type != "p":
        if type == "-1":
            return 0
        post_type = str(input("You entered wrong type, enter only 'p' for post, 'q' for question and '-1' to go back: "))
    print("Possible categories are\n", category_list.keys())
    category = str(input("Choose one of available categories for your post: "))
    checked_number = 0
    while checked_number == 0:
        for check in category_list:
            if check == category:
                if category == 'code':
                    subcategory = subcategory_program[str(input('Please choose "python" or "karel" as your subcategory'))]
                elif category == 'sections':
                    subcategory = subcategory_days[int(input("Please enter number of the day when your problem occurred")) - 1]
                checked_number = 1
            elif category == "-1":
                return 0
        if checked_number == 0:
            print("You chose unlisted category, try it again")
            category = str(input("Choose one of the listed categories: "))
    text = str(input("Input your message: "))
    print("Do you want your post to be anonymous (enter 'a') or private (enter 'p')\nFor nothing enter 'n' ", end='')
    choice = str(input())
    while True:
        if choice == 'a':
            is_anonymous = True
            break
        elif choice == 'p':
            is_private = True
            break
        elif choice == '-1':
            return 0
        elif choice == 'n':
            break
        choice = str(input("You've entered invalid input, try again: "))

    payload = {"thread": {"type": type_list[post_type], "title": title, "category": category_list[category],
                          "subcategory": subcategory, "subsubcategory": "",
                          "content": "<document version=\"2.0\"><paragraph>" + text + "</paragraph></document>",
                          "is_pinned": False, "is_private": is_private, "is_anonymous": is_anonymous,
                          "anonymous_comments": False}}
    return payload


def read(s, headers):
    amnt = str(input("How many threads would you like to display: "))
    r = s.get('https://us.edstem.org/api/courses/968/threads?limit='+amnt+'&sort=date&order=desc', headers=headers)
    website = r.json()
    threads = website['threads']
    links = []
    titles = []
    contents = []
    response = 2
    while response == 2:
        print("Would you like to read:")
        for i in range(len(threads)):
            links.append(threads[i]['id'])
            titles.append(threads[i]['title'])
            contents.append(threads[i]['content'])
            print(i+1, ": ", titles[i])
        x = int(input("Choose thread you want to read, -1 to go back: "))
        if x == -1:
            return s
        print('-------------------------------------------------------------')
        content = re.sub('<.*?>', '', contents[x-1])
        print(content)
        print('-------------------------------------------------------------')
        while 1 <= response <= 3:
            print("1 - Would you like to comment?")
            print("2 - Would you like to read another thread?")
            print("3 - Would you like to go to main menu?")
            response = int(input())
            if response == 3:
                return s
            elif response == 1:
                s = comment(s, headers, links[x-1])
                response = 2
            elif response == 2:
                pass
            else:
                print("You've entered wrong number.")


def comment(s, headers, link, message=""):
    print(link)
    print(headers)
    url = 'https://us.edstem.org/api/threads/'+str(link)+'/comments'
    if message == "":
        print("What would you like to write? Write -1 to return")
        message = str(input())
    if message == "-1":
        return s
    payload = {"comment": {"content": "<document version=\"2.0\"><paragraph>"+message+"</paragraph></document>",
                           "is_private": False, "is_anonymous": False}}
    r = s.post(url, headers=headers, json=payload)
    if r.status_code < 300:
        print('Comment sent succesfully')
        return s
    else:
        y = int(input("Something went wrong, would you like to try again(1) or cancel(0)?"))
        if y == 1:
            comment(s, headers, link, message)
        else:
            return s


def delete_thread(s, headers):
    r = s.get('https://us.edstem.org/api/courses/968/threads?filter=mine&limit=30&sort=date&order=desc', headers=headers)
    website = r.json()
    info = website['threads']
    threads = []
    links = []
    print("Would you like to delete: ")
    for i in range(len(info)):
        threads.append(info[i]['title'])
        links.append(info[i]['id'])
        print(i+1, threads[i])
    return threads, links


















if __name__ == '__main__':
    play()
