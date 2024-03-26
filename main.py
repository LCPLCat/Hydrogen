from App import create_app
from flask import Flask
from waitress import serve
dev = True
if __name__=='__main__':
    app=create_app()
    if dev == True:
        app.run(debug=True)
    else:
        serve(app, host='0.0.0.0', port=25565, threads = 10)
