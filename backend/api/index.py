from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/api/clone", methods=["POST"])
def clone_system():
    data = request.json
    return jsonify({
        "status": "success",
        "message": f"System {data.get('system_name', 'unknown')} cloned securely!"
    })

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "FolderFirewall backend is alive."})

if __name__ == "__main__":
    app.run()
