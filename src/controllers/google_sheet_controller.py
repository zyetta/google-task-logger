import gspread


class GoogleSheetController:
    gc = ""
    gc_payload = []

    def __init__(self, filename):
        self.gc = gspread.service_account(filename=filename)

    def insert_entry(self, payload):
        sh = self.gc.open("Logged Tasks")
        worksheet = sh.worksheet("Data")
        worksheet.append_rows(payload)

    def reset_payload(self):
        self.gc_payload = []
