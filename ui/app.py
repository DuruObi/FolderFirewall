from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>FolderFirewall UI</h1><p>Secure Cloning & Protection Running.</p>"

if __name__ == "__main__":
    app.run()
