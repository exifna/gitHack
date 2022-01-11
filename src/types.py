from enum import Enum


class FirstHash:
    def __init__(self, last_hash: str, _hash: str, user: str, mail: str, time: int, hour: str, commit_message: str):
        self.last_hash = last_hash
        self._hash = _hash
        self.user = user
        self.mail = mail
        self.time = time
        self.hour = hour
        self.commit_message = commit_message


class LogTypes(Enum):
    System = 0
    Exception = 1
    Info = 2


class GitObjectType(Enum):
    blob = 0
    tree = 1


class SimpleGitObject:
    def __init__(self, Type: GitObjectType, _hash: str, name: str):
        self.Type = Type
        self._hash = _hash
        self.name = name

ignore = [
    '.css', '.js', '.ttf', '.png', '.ico', '.jpeg', '.jpg'
]


label = """   _____ _ _   _    _            _    
  / ____(_) | | |  | |          | |   
 | |  __ _| |_| |__| | __ _  ___| | __
 | | |_ | | __|  __  |/ _` |/ __| |/ /
 | |__| | | |_| |  | | (_| | (__|   < 
  \_____|_|\__|_|  |_|\__,_|\___|_|\_\\
  
  
"""