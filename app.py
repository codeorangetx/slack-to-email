import sendgrid, os
from flask_slack import Slack
from flask import Flask

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
EMAIL_SLASH_TOKEN = os.environ.get('EMAIL_SLASH_TOKEN')
TEAM_ID = os.environ.get('TEAM_ID')

app = Flask(__name__)
app.config['TEAM_ID'] = TEAM_ID
slack = Slack(app)


sg = sendgrid.SendGridClient(SENDGRID_API_KEY)

@slack.command(command='email', token=os.environ.get('EMAIL_SLASH_TOKEN'), team_id=os.environ.get('TEAM_ID'), methods=['POST'])
def email_command(**kwargs):
    text = kwargs.get('text')
    status, msg = send_email(text)
    return slack.response(msg)


def send_email(body) :
    message = sendgrid.Mail(to='moizrizvi@gmail.com', subject='Code Orange Update', text=body, from_email='info@codeorange.io')
    return sg.send(message)


app.add_url_rule('/send', view_func=slack.dispatch)

if __name__ == '__main__':
    app.run(debug=True)
