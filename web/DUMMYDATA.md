# All Routes:

    Routes:

    'POST - api/v1/auth/register - BODY:{"email": "**Your Email Here**", "password": "**Your Password Here**"}
        -> This route will register an account in the database and return a session bearer token.

    'POST - api/v1/auth/login - BODY:{"email": "**Your Email Here**", "password": "**Your Password Here**"}
        -> This route will login to an existing account in the database and return a session bearer token.

    'POST - api/v1/analysis - BODY:{"text": "**Your Text Here**"}
        -> This route will take in text and return a sentiment analysis using NLTK.
        -> Each sentence will be analyzed for sentiment, as well as the entire body of the text.

    'GET - api/v1/users
        -> This route will return the email and database ID of all users registered in the database.

    'GET - api/v1/charts/{graph_type}
        -> This route will return all of the analysis that are stored in the database for the user logged in.
        -> {graph_type}: stacked_bar

    'DELETE - api/v1/admin/delete/{user_id} - {"email": "**Admin Email**", "password": "**Admin Password**"}
        -> This route will delete a singe user based on database id. Only admins can access this route.

    'GET - api/v1/admin/{graph_type}/{id}
        -> This route will retrieve all of a users data if their ID is specificed.
        -> This route will retrieve all of the aggregate data from the website if no ID is specified.
        -> This route is Admin access only.
        -> {graph_type}: stacked_bar, compound_bar, pie




# Example Analysis Input (JSON):

{"text": "The rank and file of the FBI are great people who are disgusted with what they are learning about Lyin’ James Comey and the so-called “leaders” of the FBI. Twelve have been fired or forced to leave. They got caught spying on my campaign and then called it an investigation. Bad!"}



# Example Analysis Output:

{
    "Sentences": {
        "0": [
            "The rank and file of the FBI are great people who are disgusted with what they are learning about Lyin’ James Comey and the so-called “leaders” of the FBI.",
            {
                "neg": 0.099,
                "neu": 0.783,
                "pos": 0.119,
                "compound": 0.1779
            }
        ],
        "1": [
            "Twelve have been fired or forced to leave.",
            {
                "neg": 0.609,
                "neu": 0.391,
                "pos": 0,
                "compound": -0.7783
            }
        ],
        "2": [
            "They got caught spying on my campaign and then called it an investigation.",
            {
                "neg": 0,
                "neu": 1,
                "pos": 0,
                "compound": 0
            }
        ],
        "3": [
            "Bad!",
            {
                "neg": 1,
                "neu": 0,
                "pos": 0,
                "compound": -0.5848
            }
        ]
    },
    "Body": {
        "neg": 0.234,
        "neu": 0.702,
        "pos": 0.064,
        "compound": -0.8718
    }
}
