import socket, cgi

SERVER = False ##Bei True: Rechner fungiert als Server -> von anderen lokalen Geräten erreichbar
IP = socket.gethostbyname(socket.gethostname())

HTML = {ord('ü'): '&uuml;',ord('Ü'): '&Uuml;',ord('ä'): '&auml;',ord('Ä'): '&Auml;',ord('ö'): '&ouml;',ord('Ö'): '&Ouml;',ord('ß') :'&szlig;'}

FORMULAR = """
<html>
    <head>
        <title>Formular</title>
        <link rel="stylesheet" href="https://lkunited.pythonanywhere.com/static/style.css"/>
        <meta name="author" content="Leander Kafemann"/>
    </head>
    <body>
        <div class="centerer">
            <div class="login_box">
                <div class="clearfix">
                    <h2>Formular</h2>
                    <form method="post" action="http://localhost:8000/eval?count={}">
                        <input type="text" name="name" placeholder="Nutzername"/><br/>
                        {}<br/>
                        <label for="x1"><a href="http://localhost:8000/form?count={}#focussed">Eingabefeld hinzufügen</a></label><br/>
                        <input type="password" name="code" placeholder="Passwort"/><br/>
                        <input type="submit" class="login_button" value="Absenden"/>
                    </form>
                </div>
            </div>
        </div>
    </body>
</html>
"""
F_INSERT = """<input type="text" name="x{}" placeholder="Weitere Eingabe {}"/>"""
F_INSERT_FOCUSSED = """<input type="text" name="x{}" placeholder="Weitere Eingabe {}" id="focussed"/>"""

EVALUATE = """
<html>
    <head>
        <title>Formular</title>
        <link rel="stylesheet" href="https://lkunited.pythonanywhere.com/static/style.css"/>
        <meta name="author" content="Leander Kafemann"/>
    </head>
    <body>
        <div class="centerer">
            <div class="login_box">
                <div class="clearfix">
                    <h3>
                        {}
                    </h3>
                </div>
            </div>
        </div>
    </body>
</html>"""
EVALUATE_INSERT = """Vielen Dank für die Teilnahme.<br/>Eingaben:<br/><br/>{}"""
EVALUATE_INSERT_ERROR = """<font color="red">Ein Fehler ist aufgetreten.</font>"""

def get_form(env):
    form = cgi.FieldStorage(fp=env.get("wsgi.input"), environ=env, keep_blank_values=True)
    try:
        count = int(form.getvalue("count"))
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

def evaluate_form(env):
    form = cgi.FieldStorage(fp=env.get("wsgi.input"), environ=env, keep_blank_values=True)
    try:
        format_str = ""
        format_str += form.getvalue("name")+"; "
        format_str += form.getvalue("code")+"; "
        for i in range(1, int(form.getvalue("count"))+1):
            format_str += form.getvalue("x"+str(i))+"; "
        return EVALUATE.format(EVALUATE_INSERT.format(format_str))
    except:
        return EVALUATE.format(EVALUATE_INSERT_ERROR.format("Fehler."))

def application(environ, start_response):
    global logged, actname
    status = "200 OK"
    match environ["PATH_INFO"]:
        case "/form":
            content = get_form(environ)
        case "/eval":
            content = evaluate_form(environ)
        case "/help":
            content = """<html><body>Diese Seite existiert nur zu Testzwecken.<br/>Sie finden das Formular unter <a href="http://localhost:8000/form?count=0">dieser</a> Adresse.</body></html>"""
        case _:
            status = "404 NOT FOUND"
            content = """<html><body>Seite nicht gefunden. Kontaktieren Sie einen Admin!<br/><a href="http://localhost:8000/help">Hilfe</a></body></html>"""
    response_headers = [("Content-Type", "text/html"),\
                        ("Content-Lenght", str(len(content)))]
    start_response(status, response_headers)
    if SERVER:
        content = content.replace("localhost", IP)
    content = content.translate(HTML)
    return [content.encode("utf8")]

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    port = 8000
    httpd = make_server("", port, application)
    print(f"Serving on port {port}...")
    httpd.serve_forever()
