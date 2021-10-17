from flask import Flask, jsonify, request

import json
import os

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

@app.route("/", methods = ["POST", "GET"])
def root():
    if request.method == "GET":
        return jsonify({
            "success": True,
            "message": "Welcome!",
            "endpoint": {
                "/": {
                    "POST": {
                        "form": {
                            "id": "user id",
                            "pass": "user password"
                        }
                    },
                    "GET": "This page"
                }
            }
        })
    elif request.method == "POST":
        user_form = request.json or request.form
        user_id = user_form["id"] or user_form.get("id")
        user_pass = user_form["pass"] or user_form.get("pass")
        user = None

        if user_id == None or user_pass == None:
            return jsonify({
                "error": True,
                "message": "Please fill all required form!"
            }), 400

        db = json.load(open("./db/db.json"))

        try:
            user = db[str(user_id)]
        except KeyError:
            return jsonify({
                "error": True,
                "message": "User ID not found!"
            }), 401
        
        if user["pass"] != user_pass:
            return jsonify({
                "error": True,
                "message": "Password incorrect!"
            }), 401

        return jsonify(user)

@app.errorhandler(404)
def not_found(error):
    print(error)
    return jsonify({
        "error": True,
        "message": "404 page not found!"
    }), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=False)