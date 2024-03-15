How to use the Client:

Commands:

Login : Usage is "login <url>", where <url> is to be replaced with the site you wish to login to.
        Logs the user into the requested service.

Logout: Usage is "logout".
        Logs the user out of the current service.

List: Usage is "list".
        Displays a list of all available services in the directory.

News: Usage is "news [-id=<Agency Code>] [-cat=<Category>] [-reg=<Region>] [-date=<Date>]". All options in [] 
            are optional and can be omitted, in this case it will display all stories of this parameter.
            Parameters in <> can be replaced with options:
            -id : Used to filter stories from a specific agency.
            -cat : Used to filter stories from a specific Category.
            -reg : Used to filter stories from a specific Region.
            -date : Used to filter stories from a specific Date onwards.

Post: Usage is "post".
        Allows an author to post to the requested service. Will bring up prompts for the information
        required for the post.

Delete: Usage is "delete <storyID>".
        This allows an author to delete a story they have previously posted, based on the ID provided.

Exit: Usage is "exit".
        Allows the user to exit the client application.



Domain:

sc21dc.pythonanywhere.com


Module Leader account details:

Username: ammar
Password: webServices123


Extra Information:

Any required depenecies can be found in the requirements.txt of both the client and API directories.
Client application usage: "python(3) client.py"