import sendgrid, os
from flask_slack import Slack
from flask import Flask

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
EMAIL_SLASH_TOKEN = os.environ.get('EMAIL_SLASH_TOKEN')
TEAM_ID = os.environ.get('TEAM_ID')

app = Flask(__name__)
slack = Slack(app)

sg = sendgrid.SendGridClient(SENDGRID_API_KEY)

@slack.command(command='email', token=EMAIL_SLASH_TOKEN, team_id=TEAM_ID, methods=['POST'])
def email_command(**kwargs):
    text = kwargs.get('text')
    msg = send_email(text)
    return slack.response(msg)


emails = ['moizrizvi@gmail.com', 'vparam15@gmail.com', 'raunaqsrivastava@gmail.com']

def send_email(body) :
    responses = []
    for email in emails :
        message = sendgrid.Mail(to='moizrizvi@gmail.com', subject='Code Orange Update', text=body, from_email='info@codeorange.io')
        responses += sg.send(message)[0]
    if all(response == "200" for response in responses) :
        return "Successfully sent messages."
    else :
        return "Something fucked up... sorry :-("


app.add_url_rule('/send', view_func=slack.dispatch)

if __name__ == '__main__':
    app.run(debug=True)
