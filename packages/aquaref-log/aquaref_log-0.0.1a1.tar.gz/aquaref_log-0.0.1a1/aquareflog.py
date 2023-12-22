from os import environ
from colorama import Fore

environ["AQUAREF.LOG"] = ""


def _Log(Log, ForeColor=None):
    def Print(Log, ForeColor):
        from colorama import Fore
        from time import localtime
        import datetime

        if ForeColor is None:
            ForeColor = "RESET"

        t = localtime()
        now = datetime.datetime.combine(datetime.date(t.tm_year, t.tm_mon, t.tm_mday),
                                        datetime.time(t.tm_hour, t.tm_min, t.tm_sec))
        print(Fore.BLUE + f"Aquaref.Log {str(now)} ||" + Fore.RESET, getattr(Fore, ForeColor.upper()), Log, Fore.RESET)

        environ["AQUAREF.LOG"] += f"{str(now)} || {Log}\n"

    if "AQUAREF.LOG.ENABLE" in environ:
        if environ["AQUAREF.LOG.ENABLE"].upper() == "TRUE":
            Print(Log, ForeColor)
        else:
            pass
    else:
        Print(Log, ForeColor)


def Debug(Log):
    _Log(Log)


def Error(Log):
    _Log(Log, "RED")


def Info(Log):
    _Log(Log, "BLUE")


def Success(Log):
    _Log(Log, "GREEN")


def GetLog():
    return environ["AQUAREF.LOG"]


def SaveLog(*args, encoding="utf-8", **kwargs):
    with open(*args, mode="w+", encoding=encoding, **kwargs) as log:
        log.write(GetLog())


if __name__ == '__main__':
    Debug("Debug")
    Error("Error")
    Info("Info")
    Success("Success")

    for index in range(5):
        Debug(f"Debug{index}")

    print(GetLog())