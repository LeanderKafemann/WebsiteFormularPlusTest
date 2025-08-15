from PyWSGIRef import *

from strings import *

__version__ = "1.0.0"

for i in ["evaluate", "formular"]:
    addSchablone(i, loadFromFile("./templates/{}.pyhtml".format(i)))

# quick-access
FORMULAR = SCHABLONEN["formular"].decoded()
EVALUATE = SCHABLONEN["evaluate"].decoded()

def get_form(form: FieldStorage):
    try:
        c = form.getvalue("count")
        print(c)
        count = int(c) if c != None else 0
        if count < 0:
            raise ValueError()
        elif count == 0:
            return FORMULAR.format("0", "", "1")
        elif count == 1:
            return FORMULAR.format("1", F_INSERT_FOCUSSED.format("1", "1"), "2")
        else:
            INSTRING = ""
            for i in range(1, count):
                INSTRING += F_INSERT.format(str(i), str(i))+"<br/>"
            INSTRING += F_INSERT_FOCUSSED.format(str(count), str(count))
            return FORMULAR.format(str(count), INSTRING, str(count+1))
    except:
        return EVALUATE.format(EVALUATE_INSERT_ERROR.format("Fehler beim Zählen der Felder."))

def evaluate_form(form: FieldStorage):
    try:
        format_str = ""
        format_str += form.getvalue("name")+"; "
        format_str += form.getvalue("code")+"; "
        for i in range(1, int(form.getvalue("count"))+1):
            format_str += form.getvalue("x"+str(i))+"; "
        return EVALUATE.format(EVALUATE_INSERT.format(format_str))
    except:
        return EVALUATE.format(EVALUATE_INSERT_ERROR.format("Fehler."))

def application(path: str, fs: FieldStorage):
    match path:
        case "/form":
            return get_form(fs)
        case "/eval":
            return evaluate_form(fs)
        case "/version":
            return __version__
        case "/help":
            return ONLY_TEST
        case _:
            return NOT_FOUND
app = makeApplicationObject(application, True)

if __name__ == "__main__":
    server = setUpServer(app)
    server.serve_forever()
