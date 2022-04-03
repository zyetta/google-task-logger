import requests
from datetime import datetime


class DiscordNotifier:
    def __init__(self, webhook_url):
        self.uri = webhook_url

        message = {
            "content": "Tasks Logged | " + str(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")),
            "username": "Task Logger",
            "avatar_url": "https://i0.wp.com/9to5google.com/wp-content/uploads/sites/4/2018/03"
                          "/google_tasks_leaked_icon.jpg?w=2000&quality=82&strip=all&ssl=1",
        }
        requests.post(webhook_url, data=message)
