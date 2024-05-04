# -*-   Coding with utf-8   -*- #
# -*- Developed by Harryjin -*- #

import requests

# Information to search
def get_information():
    cat_choice = ('pol', 'art', 'tech', 'trivia', '*')
    reg_choice = ('uk', 'eu', 'w', '*')
    category = '*'
    region = '*'
    while True:
        temp = input("Choices of the category: \n1) Politics \n2) Arts \n3) New Technology \n4) Trivia \n5) All \nEnter your choice: ")
        try:
            category = cat_choice[int(temp)-1]
            break
        except Exception as e:
            print("Invalid Input! Please try again!")

    while True:
        temp = input("Choices of the region: \n1) United Kingdom \n2) Europe \n3) World \n4) All \nEnter your choice: ")
        try:
            region = reg_choice[int(temp)-1]
            break
        except Exception as e:
            print("Invalid Input! Please try again!")

    return category, region

# Information to post
def get_information_post():
    cat_choice = ('pol', 'art', 'tech', 'trivia')
    reg_choice = ('uk', 'eu', 'w')
    category = ''
    region = ''
    while True:
        temp = input("Choices of the category: \n1) Politics \n2) Arts \n3) New Technology \n4) Trivia \nEnter your choice: ")
        try:
            category = cat_choice[int(temp)-1]
            break
        except Exception as e:
            print("Invalid Input! Please try again!")

    while True:
        temp = input("Choices of the region: \n1) United Kingdom \n2) Europe \n3) World \nEnter your choice: ")
        try:
            region = reg_choice[int(temp)-1]
            break
        except Exception as e:
            print("Invalid Input! Please try again!")

    return category, region

'''
User Login
Param: login url
Return: user token or error message
'''
def login(url):
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    data = {"username": username, "password": password}
    response = requests.post(url=f"{url}/api/login/", data=data)
    if response.status_code == 200:
        print(response.json()['msg'])
        token = response.json()['token']
        print(f'Your token is: {token}')
        return token
    else:
        print("Login failed!")
        print(response.content)
        return ''

'''
User Logout
Param: URL and user token
Return: Response message
'''
def logout(url, token):
    response = requests.post(f"{url}/api/logout/", data={'token': token})
    if response.status_code == 200:
        print("Logout successful!")
    else:
        print("Logout failed!")

'''
Post new story / news
Param: URL and user token
Return: Response message
'''
def post_story(url, token):
    title = input("Enter the story title: ")
    category, region = get_information_post()
    details = input("Enter the story details: ")
    response = requests.post(f"{url}/api/stories/", data={"title": title, "category": category, "region": region, "details": details, 'token': token})
    if response.status_code == 201:
        print("Story posted successfully!")
    else:
        print("Failed to post story!")
        print(response.content)

'''
List news / stories
Param: URL
Return: Stories / Response message
'''
def get_stories(url):
    category, region = get_information()
    date = input("Enter the date you want to search (* for all): ")
    response = requests.get(f"{url}/api/stories/", data={"story_cat": category, "story_reg": region, "story_date": date})
    if response.status_code == 200:
        stories = response.json()
        for story in stories:
            print(story)
    else:
        print("Failed to get stories!")
        print(response.content)

'''
List news agencies
Param: URL
Return: News Agencies / Response message
'''
def list_agencies(url):
    response = requests.get(f"{url}/api/directory/")
    if response.status_code == 200:
        agencies = response.json()
        for agency in agencies:
            print(agency)
    else:
        print("Failed to list agencies!")
        print(response.content)

'''
Delete stories
Param: URL and user token
Return: Response message
'''
def delete_story(url, story_key, token):
    response = requests.delete(f"{url}/api/stories/{story_key}/", data={'token': token})
    if response.status_code == 200:
        print("Story deleted successfully!")
    else:
        print("Failed to delete story!")
        print(response.content)

def main():
    url = "https://example.com/"
    token = ''
    while True:
        command = input("Enter a command: ")
        if command == "login":
            token = login(url)
        elif command == "logout":
            logout(url, token)
        elif command == "post":
            post_story(url, token)
        elif command == "news":
            get_stories(url)
        elif command == "list":
            list_agencies(url)
        elif command == "delete":
            story_key = input("Enter the story key: ")
            delete_story(url, story_key, token)
        else:
            print("Unknown command!")

if __name__ == "__main__":
    main()
