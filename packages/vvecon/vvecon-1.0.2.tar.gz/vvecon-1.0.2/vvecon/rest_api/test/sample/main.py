from vvecon.rest_api import App
from Resources import User, sock, mail
from dotenv import load_dotenv
from os import environ

load_dotenv()

# initializing API
app = App(__name__)
app.mail(mail, environ.get("EMAIL"), environ.get("APP_PASSWORD"))
app.socket(sock)

# add Admin class to API resources
app.add_resource(User, "/")

if __name__ == "__main__":
    # run the server
    app.run(debug=True, port=5000)
