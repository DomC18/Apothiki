import string
import os

TASKMANAGERDIR = os.path.realpath(__file__)[:-12]
USERDATADIR = TASKMANAGERDIR + "UserData\\"
ICONDIR = TASKMANAGERDIR + "Icons\\"
ADDFILE = ICONDIR + "add.png"
DELETEFILE = ICONDIR + "delete.png"
DELETEMEDIUMFILE = ICONDIR + "deletemedium.png"
EDITFILE = ICONDIR + "edit.png"
EDITMEDIUMFILE = ICONDIR + "editmedium.png"
EDITLARGEFILE = ICONDIR + "editlarge.png"
FILTERFILE = ICONDIR + "filter.png"
FILTERLARGEFILE = ICONDIR + "filterlarge.png"
INFOFILE = ICONDIR + "info.png"
INFOLARGEFILE = ICONDIR + "infolarge.png"
PEEKFILE = ICONDIR = "peek.png"
PROFILEFILE = ICONDIR + "profile.png"
SAVEFILE = ICONDIR + "save.png"

CRED_CHARS = string.ascii_letters + string.digits + string.punctuation
LET_CHARS = string.ascii_letters
DIGIT_CHARS = string.digits