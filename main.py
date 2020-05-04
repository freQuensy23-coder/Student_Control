import config
import requests
import time
import datetime
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

def auth(CREDENTIALS_FILE):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    return apiclient.discovery.build('sheets', 'v4', http=httpAuth)


def get_spreadsheet_values(list_name:str, range:str, type:str):
    values = service.spreadsheets().values().get(
        spreadsheetId = config.spreadsheet_id,
        range = "'" + list_name + "'!" + range,
        majorDimension = type
    ).execute()
    return(values['values'])


def get_list_name():
    today = datetime.date.today()
    day = today.day
    month = today.month
    year = today.year
    return str(day) + "." + str(month) + "." + str(year)


def get_spreadsheet_data(range):
    list_name = get_list_name()
    # list_name = "Л1ист2"
    try:
        return get_spreadsheet_values(list_name, range, "ROWS")
    except:
        return []


def get_balance_text():
    debts = get_spreadsheet_data(config.balance)
    text = "*Долги*\n "
    for debt in debts:
        text += debt[0] + " - " + debt[3] + "\n"
    return text


def get_activity_text():
    text = "\n *Затраченое время*\n"
    activities = get_spreadsheet_data(config.activities)
    for activity in activities:
        if activity[0] != "":
            text += "*" + activity[0] + "*\n"
        if activity[1] != "":
            text+= "-" + activity[1] + " " + activity[2] + "ч.\n"
    return text


def get_total_activity_text():
    return  "*TOTAL: *" + get_spreadsheet_data(config.total_time)[0][0] + " ч.\n"


def get_msg_text():
    if get_spreadsheet_data(range) == []:
        text = get_balance_text() + get_activity_text() + get_total_activity_text()
    else:
        text = "Ничего не делал."
    return text


def send_msg():
    msg_text = get_msg_text()
    url = ("https://api.telegram.org/bot" + config.telegram_key + "/sendMessage?chat_id=" + config.admins_chat_id + "&text=" + msg_text + "&parse_mode=Markdown")
    r = requests.get(url, config.proxy)


CREDENTIALS_FILE = config.file
service = auth(CREDENTIALS_FILE)


while True:
    # try:
    if True:
        now = datetime.datetime.now()
        if now.hour == config.notify_hour:
            send_msg()
            time.sleep(60*60*12-100)
        else:
            print("Sleeping")
            time.sleep(2*60)

    # except:
    #     print("Error" + datetime.datetime.now)