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
user_list = slack.users.list().body['members']
emails = filter(None, [u['profile']['email'] for u in user_list])
admin = {u['id'] : u['is_admin'] for u in user_list if u['is_admin']}

sg = sendgrid.SendGridClient(SENDGRID_API_KEY)

@slash.command(command='email', token=EMAIL_SLASH_TOKEN, team_id=TEAM_ID, methods=['POST'])
def email_command(**kwargs):
    text = kwargs.get('text')

    # parses text for subject if given
    if '{' in text and '}' in text:
        beg = text.index('{')
        end = text.index('}')
    else:
        beg, end = -2, -1

    subject =   'Code Orange Update' if text[beg+1:end] is '' else text[beg+1:end]
    body =      text[end+1:]

    # check if user is admin
    user_id = kwargs.get('user_id')
    if user_id not in admin :
        return slash.response("Sorry, you must be an admin to user this command.")

    msg = send_email(subject, body)
    return slash.response(msg)

def send_email(_subject, _body) :
    responses = []
    for email in emails :
        message = sendgrid.Mail(to=email, subject=_subject, text=_body, from_email='info@codeorange.io')
        status, msg = sg.send(message)
        responses.append(status)

    if all(response == 200 for response in responses) :
        return "Successfully sent messages."
    else :
        return "Something fucked up... sorry :-("


app.add_url_rule('/send', view_func=slash.dispatch)

if __name__ == '__main__':
    app.run()
