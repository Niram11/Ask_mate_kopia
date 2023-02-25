from datetime import datetime

def get_timestamp():
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y %H:%M")
    return str(timestamp)

