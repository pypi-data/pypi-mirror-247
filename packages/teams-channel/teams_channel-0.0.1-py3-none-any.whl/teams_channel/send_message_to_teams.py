import pymsteams
def send_message_to_teams(webhook_key, comment):
    myTeamsMessage = pymsteams.connectorcard(webhook_key)
    myTeamsMessage.text(comment)
    myTeamsMessage.send()