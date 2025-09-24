from flask import Flask
app = Flask(__name__)
@app.route("/")
def home():
    return "<h1>FolderFirewall Demo</h1><p>UI prototype running on Vercel.</p>"
if __name__ == "__main__":
    app.run()
