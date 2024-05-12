import string
import os

TASKMANAGERDIR = os.path.realpath(__file__)[:-12]
USERDATADIR = TASKMANAGERDIR + "UserData\\"
ICONDIR = TASKMANAGERDIR + "Icons\\"

PASSWORD_CHARS = string.ascii_letters + string.digits + string.punctuation