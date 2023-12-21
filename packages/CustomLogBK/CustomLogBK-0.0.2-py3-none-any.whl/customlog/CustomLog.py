from datetime import datetime as dtt

class CustomLog:
    def __init__(self, d_log: str, name_prg: str) -> None:
        self.d_log: str = d_log
        self.name_prg: str = name_prg

    def write(self, log: str = ''):
        today = dtt.today()
        full_date = today.strftime("%d/%m/%Y A %H:%M:%S")
        short_date = today.strftime("%Y%m%d")
        log_file = fr"{self.d_log}/{short_date}_{self.name_prg}.log"
        if log == '':
            log = "*" * 40
        enr = f"Le {full_date}\t{log}"
        if log[0:1] == '-':
            enr = f"{log[1:len(log)]}"
        with open(log_file, "a", encoding="utf-8") as fl:
            fl.write(f"{enr}\n")
        print(enr)
