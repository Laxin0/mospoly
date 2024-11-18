from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
types = ["лек", "пр", "СР"]
ranks = ["ст пр", "доц"]
OUT_PATH = "out.txt"
start_date = datetime.strptime("16.09.2023", "%d.%m.%Y")
end_date = datetime.strptime("28.12.2023", "%d.%m.%Y")
year = ".2023"
@dataclass
class Lesson():
    def __init__(self, s, ty, te, r, ti):
        self.subject = s
        self.typ = ty
        self.teacher = te
        self.room = r
        self.time = ti

    def __str__(self) -> str:
        return str((
            self.subject,
            self.typ, 
            self.teacher, 
            self.room,
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
    info = {TokenType.TIME: None,
            TokenType.TYPE: None,
            TokenType.TEACH: None,
            TokenType.SUBJ: None,
            TokenType.ROOM: None,
            TokenType.DATES:None}
    match tokens[i].typ, tokens[i+1].typ:
        case TokenType.TIME, TokenType.SUBJ:
            info[TokenType.TIME] = tokens[i].val
            info[TokenType.SUBJ] = tokens[i+1].val
            i += 2
        case TokenType.SUBJ, _:
            info[TokenType.TIME] = infos[-1][TokenType.TIME]
            info[TokenType.SUBJ] = tokens[i].val
            i += 1
        case _, _:
            info[TokenType.TIME] = infos[-1][TokenType.TIME]
            info[TokenType.SUBJ] = infos[-1][TokenType.SUBJ]

    while i < len(tokens):
        tok = tokens[i]
        if info[tok.typ] != None:
            infos.append(info)
            break

        info[tok.typ] = tok.val
        i += 1

for i in range(len(infos)):
    if not infos[i][TokenType.TEACH]:
        infos[i][TokenType.TEACH] = infos[i-1][TokenType.TEACH]

def generate_dates(start, end):
    dates = []
    date = start
    while date <= end:
        if date.weekday() != 6:
            dates.append(date.strftime("%d.%m"))
        date += timedelta(days=1)
    return dates

def parse_dates(s: str):
    elements = s.replace(':', ';').replace(',', '.').split(';')
    for i in elements:
        if "--" in i:
            bounds = i.split("--")
            try:
                start = datetime.strptime(bounds[0]+year, "%d.%m.%Y")
                end = datetime.strptime(bounds[1]+year, "%d.%m.%Y")
            except:
                error(f"Invalid date range in\n`{i}`")
            return generate_dates(start, end)

        else:
            try:
                date = datetime.strptime(i+year, "%d.%m.%Y")
            except:
                error(f"Invalid date in\n`{i}`")
            return [date]

days = {}
for i in infos:
    dates = i[TokenType.DATES]
    for d in parse_dates(dates):
        if d in days.keys():
            days[d].append(i)
        else:
            days.update({d: [i]})
with open(OUT_PATH, "w") as f:
    
    dates = generate_dates(start_date, end_date)
    #print(dates)
    f.write("\t")
    f.write("\t".join([d.strftime("%d.%m")]))
    for time in ["8:30-10:00", "10:20-11:50", "12:30-14:00", "14:20-15:50", "16:10-17:40", "17.50-19:20", "19:30-21:00"]:
        f.write(time)
        f.write("\t")
        for date in dates:
            if date in days.keys():
                day = days[date]
                lesson = ""
                for l in day:
                    if l[TokenType.TIME] == time:
                        lesson = l[TokenType.SUBJ]
                f.write(lesson)
            f.write("\t")
        f.write("\n")


