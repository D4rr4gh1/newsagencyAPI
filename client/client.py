import requests
from getpass import getpass

URL = None

session = requests.Session()

def login(username, password):
    try:
        response = session.post(f"{URL}/api/login", data={"username" : username, "password" : password}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    except Exception as e:
        print(f"Login Failed: {str(e)}")
        return
    print(response.text)

def logout():
    try:
        response = session.post(f"{URL}/api/logout")
    except Exception as e:
        print(f"Failed to logout: {str(e)}")
        return
    print(response.text)
    

def post():
    headline = input("Headline: ")
    category = input("Category: ")
    region = input("Region: ")
    details = input("Details: ")

    try:
        response = session.post(f"{URL}/api/stories", json={"headline" : headline, "category" : category, "region" : region, "details" : details})
    except Exception as e:
        print(f"Failed to post story: {str(e)}")
        return
    print(response.text)

def news(id=None, category="*", region="*", date="*"):
    response = requests.get("https://newssites.pythonanywhere.com/api/directory")

    if id != None:
        site = next((site for site in response.json() if site['agency_code'] == id), None)
        if site:
            response = requests.get(f"{site['url']}/api/stories", data={"story_cat" : category, "story_region" : region, "story_date" : date}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
            if response.status_code != 200:
                print(f"Failed to get news: {response.text}")
                return
            
            if response.json()['stories'] == []:
                print("No stories found")
                return
            for story in response.json()['stories']:
                print("--------------------------------------------------")
                print(f"Headline:  {story['headline']}")
                print(f"Category:  {story['story_cat']}")
                print(f"Region:  {story['story_region']}")
                print(f"Author:  {story['author']}")
                print(f"Date:  {story['story_date']}")
                print(f"Details:  {story['story_details']}")
            
        else:
            print("Invalid Agency Code")
            return
        
    else:
        for site in response.json():
            print("")
            print("")
            print("-----------------AGENCY:------------------------")
            print(f"Agency Name:  {site['agency_name']}")
            print(f"Agency Code:  {site['agency_code']}")
            print(f"URL:  {site['url']}")
            print("--------------------------------------------------")
            response = requests.get(f"{site['url']}/api/stories", data={"story_cat" : category, "story_region" : region, "story_date" : date})
            if response.status_code != 200:
                print(f"Failed to get news: {response.text}")
                continue
            
            if response.json()['stories'] == []:
                print("No stories found")
                continue
            
            print("-----------------STORIES:------------------------")
            for story in response.json()['stories']:
                print("--------------------------------------------------")
                print(f"Headline:  {story['headline']}")
                print(f"Category:  {story['story_cat']}")
                print(f"Region:  {story['story_region']}")
                print(f"Author:  {story['author']}")
                print(f"Date:  {story['story_date']}")
                print(f"Details:  {story['story_details']}")

    
    return

def list():
    response = requests.get("https://newssites.pythonanywhere.com/api/directory")
    for site in response.json():
        print("--------------------------------------------------")
        print(f"Agency Name:  {site['agency_name']}")
        print(f"Agency Code:  {site['agency_code']}")
        print(f"URL:  {site['url']}")
    
    return

def delete(storyID):
    response = session.delete(f"{URL}/api/stories/{storyID}")
    
    print(response.text)


def main():

    global URL
    loop = True

    while loop:
        userInput = input("Please enter a command: ")
        args = userInput.split()
        command = args[0].lower()

        match command:
            case "login":
                if len(args) != 2:
                    print("Invalid number of arguments. Usage is login <URL>")
                    
                else:
                    URL = "http://" + args[1]
                    username = input("Username: ")
                    password = getpass("Password: ")
                    login(username, password)          
                continue
            case "logout":
                if URL == None:
                    print("You are not logged in")
                    continue
                logout()
                URL=None
                continue
            case "post":
                if URL == None:
                    print("You are not logged in")
                    continue
                post()
                continue
            case "news":
                id, category, region, date = None, "*", "*", "*"
                for arg in args[1:]:
                    if arg.startswith("-id="):
                        id = arg.split("=")[1]
                    elif arg.startswith("-cat="):
                        category = arg.split("=")[1]
                    elif arg.startswith("-reg="):
                        region = arg.split("=")[1]
                    elif arg.startswith("-date="):
                        date = arg.split("=")[1]
                news(id, category, region, date)
                continue
            case "list":
                list()
                continue
            case "delete":
                if URL == None:
                    print("You are not logged in")
                    continue
                if len(args) != 2:
                    print("Invalid number of arguments")
                
                if not args[1].isdigit():
                    print("Invalid story ID. Must be a digit")
                
                else:
                    # print(args[1])
                    delete(args[1])
                continue
            case "exit":
                loop = False
                continue
        print("Invalid command")


    return

if __name__ == "__main__":
    main()