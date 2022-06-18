from src.controllers.sqlite_controller import SqliteController as Sql
from src.controllers.google_sheet_controller import GoogleSheetController as GSheet
from src.models.task_model import Tasks
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from src.utils.notifications import DiscordNotifier
from dotenv import load_dotenv


load_dotenv()
if __name__ == "__main__":
    absolute_dir = os.path.dirname(os.path.realpath(__file__))
    sql_controller = Sql(f"{absolute_dir}/data.db")
    gs_controller = GSheet(f"{absolute_dir}/{os.getenv('CREDS_FILENAME')}")
    SCOPES = ["https://www.googleapis.com/auth/tasks.readonly"]
    creds = None

    if os.path.exists(f"{absolute_dir}/token.json"):
        creds = Credentials.from_authorized_user_file(
            f"{absolute_dir}/token.json", SCOPES
        )
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                f"{absolute_dir}/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(f"{absolute_dir}/token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("tasks", "v1", credentials=creds)
        task_lists_results = service.tasklists().list(maxResults=10).execute()
        task_lists = task_lists_results.get("items", [])
        for i in task_lists:
            tasks = (
                service.tasks()
                .list(tasklist=i["id"], showCompleted=True, showHidden=True)
                .execute()
            )
            for j in tasks["items"]:
                if j["status"] == "completed":
                    task = Tasks(
                        task_id=j["id"],
                        title=j["title"],
                        task_list=i["title"],
                        completed=j["completed"],
                    )
                    entry_exists = sql_controller.get_task(task.get_id())
                    if entry_exists:
                        print(
                            f"Task exists. Skipping.\t\t{json.dumps(task.get_task())}"
                        )
                    else:
                        insert_success = sql_controller.insert_task(task.get_task())
                        if not insert_success:
                            print(
                                f"Could not insert task:\t{json.dumps(task.get_task())}"
                            )
                        else:
                            task_data = task.get_task()
                            gs_controller.gc_payload.append(
                                [
                                    task_data["id"],
                                    task_data["task_id"],
                                    task_data["title"],
                                    task_data["task_list"],
                                    task_data["completed"],
                                ]
                            )
            if len(gs_controller.gc_payload) > 0:
                print("Uploading Data to Google Cloud")
                gs_controller.insert_entry(gs_controller.gc_payload)
                gs_controller.reset_payload()
            else:
                print("No Data to Upload")
        discord_handler = DiscordNotifier(os.getenv("DISCORD_URL"))
    except HttpError as err:
        print(err)
