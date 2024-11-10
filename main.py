from dataclasses import dataclass

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

table = []

with open("sh.txt", encoding="utf-8") as f:
    for l in f.readlines():
        if isspaceorempty(l): continue
        table.append(l.split("\t"))

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

infos = []

i = 0
while i < len(table):
    info = Info()
    _, time, inf, room = table[i]
    sub = parse_subject(inf)
    info.subject = sub
    if sub:
        while not info.is_filled():
            _, time, inf, room = table[i]
            if not info.time:    info.time    = time if not isspaceorempty(time) else None
            if not info.room:    info.room    = room if not isspaceorempty(room) else None
            if not info.teacher: info.teacher = parse_teacher(inf)
            if not info.dates:   info.dates   = parse_dates(inf)
            if not info.typ:     info.typ     = parse_type(inf)
            i += 1
    else:
        while not parse_subject(inf) and i < len(table):
            _, time, inf, room = table[i]
            if not info.time:info.time = time if not isspaceorempty(time) else None
            if not info.room:info.room    = room if not isspaceorempty(room) else None
            if not info.teacher:info.teacher = parse_teacher(inf)
            if not info.dates:info.dates   = parse_dates(inf)
            if not info.typ:info.typ     = parse_type(inf)
            i += 1
        i -= 1

    infos.append(info)

for i in infos:
    print(i)