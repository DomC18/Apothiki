import string
import os

TASKMANAGERDIR = os.path.realpath(__file__)[:-12]
USERDATADIR = TASKMANAGERDIR + "UserData\\"
ICONDIR = TASKMANAGERDIR + "Icons\\"

CRED_CHARS = string.ascii_letters + string.digits + string.punctuation
LET_CHARS = string.ascii_letters
DIGIT_CHARS = string.digits