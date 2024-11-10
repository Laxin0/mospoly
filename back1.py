from dataclasses import dataclass
from enum import Enum

types = ["лек", "пр", "СР"]
ranks = ["ст пр", "доц"]

@dataclass
class Info():
    def __init__(self):
        self.subject = None
        self.typ = None
        self.teacher = None
        self.room = None
        self.dates = None
        self.time = None

    def is_filled(self) -> bool:
        return all((
            self.subject,
            self.typ, 
            self.teacher, 
            self.room,
            self.dates,
            self.time
        ))

    def __str__(self) -> str:
        return str((
            self.subject,
            self.typ, 
            self.teacher, 
            self.room,
            self.dates,
            self.time
        ))

def error(msg: str):
    print(f"[ERROR]: {msg}")
    exit(1)
    
def isspaceorempty(s: str) -> bool:
    return s.isspace() or s == ""

def parse_teacher(s: str) -> str|None:
    start = None
    for r in ranks:
        if f"{r} " in s:
            start = s.find(r)+len(r)+1
            break
    else:
        return None
    end = s.find(" ", s.find(" ", start)+1)
    if end < 0:
        error("Shit happened")
    return s[start:end]
    


def parse_dates(s: str) -> str|None:
    for i in range(len(s)):
        if str.isdigit(s[i]):
            return s[i:]
        
    return None

def parse_subject(s: str) -> str:
    for i in s:
        if not(i.isalpha() or i in " ()"):
            return None
    return s

def parse_type(s : str) -> str|None:
    for t in types:
        if f"/{t}/" in s:
            return t
        
    return None

class TokenType(Enum):
    TIME  = 0
    TYPE  = 1
    TEACH = 2
    SUBJ  = 3
    ROOM  = 4
    DATES = 5

class Token():
    typ: TokenType
    val: str

    def __init__(self, typ, val):
        self.typ = typ
        self.val = val

    def __str__(self) -> str:
        return f"{self.typ.name}: '{self.val}'"

infos = []
tokens = []

with open("sh.txt", encoding="utf-8") as f:
    for l in f.readlines():
        if isspaceorempty(l): continue
        _, time, inf, room = l.split("\t")

        if time:                        tokens.append(Token(TokenType.TIME, time))
        if sub   := parse_subject(inf): tokens.append(Token(TokenType.SUBJ, sub))
        if teach := parse_teacher(inf): tokens.append(Token(TokenType.TEACH, teach))
        if typ   := parse_type(inf):    tokens.append(Token(TokenType.TYPE, typ))
        if dates := parse_dates(inf):   tokens.append(Token(TokenType.DATES, dates))
        if not isspaceorempty(room):    tokens.append(Token(TokenType.ROOM, room.rstrip()))
i = 0
while i < len(tokens):
    info = {TokenType.TIME:None, TokenType.TYPE:None, TokenType.TEACH:None, TokenType.SUBJ:None, TokenType.ROOM:None, TokenType.DATES:None}
    while True:
        tok = tokens[i]
        i+=1
        if all(info.values()) or info[tok.typ] or i >= len(tokens):
            break
        info[tok.typ] = tok.val
    infos.append(info)

for t in tokens:
    print(t)

                
