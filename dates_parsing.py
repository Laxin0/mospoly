def error(msg):
    print(msg)
    exit(1)
def parse_dates(s: str):
    elements = s.replace(':', ';').replace(',', '.').split(';')
    for i in elements:
        if "--" in i:
            bounds = i.split("--")
            print(bounds)
            start = end = None
            try:
                start = datetime.strptime(bounds[0], "%d.%m")
                end = datetime.strptime(bounds[1], "%d.%m")
            except:
                error(f"Invalid date range in `{i}`")
            return gen_dates(start, end)

        else:
            date = None
            try:
                date = datetime.strptime(i, "%d.%m")
            except:
                error(f"Invalid date in `{i}`")
            return [date]


print(parse_dates("16.09--7.10;21.10;28.10;11.11--23.12"))
