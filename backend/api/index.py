from flask import Flask, jsonify, request
app = Flask(__name__)
@app.route("/api/health")
def health():
    return jsonify({"status":"ok","message":"FolderFirewall demo alive"})
@app.route("/api/clone", methods=["POST"])
def clone():
    data = request.json or {}
    return jsonify({"status":"ok","system": data.get("system_name","demo")})
if __name__ == "__main__":
    app.run()
