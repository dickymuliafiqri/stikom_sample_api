from flask import Flask, jsonify, request

import json
import os

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

@app.route("/", methods=["POST", "GET"])
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
        user_form = request.form
        user_id = user_form.get("id")
        user_pass = user_form.get("pass")
        user = None

        if user_id == None or user_pass == None:
            return jsonify({
                "error": True,
                "message": "Please fill all required form!"
            })

        db = json.load(open("./db/db.json"))

        try:
            user = db[user_id]
        except KeyError:
            return jsonify({
                "error": True,
                "message": "User ID not found!"
            })
        
        if user["pass"] != user_pass:
            return jsonify({
                "error": True,
                "message": "Password incorrect!"
            })

        return jsonify(user)

    else:
        return jsonify({
            "error": True,
            "message": "only post and get method allowed!"
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=False)