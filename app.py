from flask import Flask, request, jsonify
from models import db, FeatureFlag

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flags.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/flags", methods=["POST"])
def create_flag():

    data = request.get_json()

    flag = FeatureFlag(
        name=data["name"],
        enabled=data.get("enabled", False)
    )

    db.session.add(flag)
    db.session.commit()

    return jsonify({
        "message": "Feature flag created"
    })


@app.route("/flags/<name>")
def get_flag(name):

    flag = FeatureFlag.query.filter_by(
        name=name
    ).first()

    if not flag:
        return jsonify({
            "message": "Feature not found"
        }), 404

    return jsonify({
        "feature": flag.name,
        "enabled": flag.enabled
    })


@app.route("/flags/<name>", methods=["PUT"])
def update_flag(name):

    flag = FeatureFlag.query.filter_by(
        name=name
    ).first()

    if not flag:
        return jsonify({
            "message": "Feature not found"
        }), 404

    data = request.get_json()

    flag.enabled = data["enabled"]

    db.session.commit()

    return jsonify({
        "message": "Feature updated"
    })


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(debug=True)
