import sendgrid, os
from flask_slack import Slack
from flask import Flask
from slacker import Slacker
import time

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
EMAIL_SLASH_TOKEN = os.environ.get('EMAIL_SLASH_TOKEN')
SLACK_API_TOKEN = os.environ.get('SLACK_API_TOKEN')
TEAM_ID = os.environ.get('TEAM_ID')

app = Flask(__name__)
slash = Slack(app)
slack = Slacker(SLACK_API_TOKEN)

# Get list of users in slack org
user_list = slack.users.list()
emails = filter(None, [u['profile']['email'] for u in user_list.body['members']])

sg = sendgrid.SendGridClient(SENDGRID_API_KEY)

@slash.command(command='email', token=EMAIL_SLASH_TOKEN, team_id=TEAM_ID, methods=['POST'])
def email_command(**kwargs):
    text = kwargs.get('text')
    msg = send_email(text)
    return slash.response(msg)

def send_email(body) :
    responses = []
    for email in emails :
        message = sendgrid.Mail(to=email, subject='Code Orange Update', text=body, from_email='info@codeorange.io')
        status, msg = sg.send(message)
        responses.append(status)
    
    if all(response == 200 for response in responses) :
        return "Successfully sent messages."
    else :
        return "Something fucked up... sorry :-("


app.add_url_rule('/send', view_func=slash.dispatch)

if __name__ == '__main__':
    app.run()
