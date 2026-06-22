import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEMBER_FILE = os.path.join(BASE_DIR, "db", "members.json")
INTRUSION_LOG_FILE = os.path.join(BASE_DIR, "db", "intrusion_log.json")

def load_members():

    try:
        with open(MEMBER_FILE, encoding = 'utf-8') as f:
            return json.load(f)

    except:
        return {}

def save_members(members):

    with open(MEMBER_FILE, "w", encoding='utf-8') as f:
        json.dump(
            members,
            f,
            ensure_ascii = False,
            indent = 4
        )

def load_intrusion_logs():

    try:
        with open(INTRUSION_LOG_FILE, encoding='utf-8') as f:
            return json.load(f)

    except:
        return []


def save_intrusion_logs(logs):

    with open(INTRUSION_LOG_FILE, "w", encoding='utf-8') as f:
        json.dump(
            logs,
            f,
            ensure_ascii=False,
            indent=4
        )