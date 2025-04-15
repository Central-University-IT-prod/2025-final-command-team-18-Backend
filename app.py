from flask import jsonify, abort, send_from_directory
from manage import app, db, redis_client
from config import SERVER_HOST, SERVER_PORT, APP_DEBUG, UPLOADFLOADER
from blueprints import client, company, loyal, qr_process, stats
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, get_jwt, set_access_cookies, unset_jwt_cookies

app.register_blueprint(client, url_prefix='/clients')
app.register_blueprint(company, url_prefix='/company')
app.register_blueprint(loyal, url_prefix='/loyal')
app.register_blueprint(qr_process, url_prefix="/qr")
app.register_blueprint(stats, url_prefix="/stats")


@app.route('/ping')
def ping():
    return "PROoooooDoODODoANO", 200


@app.route("/test/drop-db", methods=["POST"])
def drop_db():
    if not app.debug:
        abort(404)
    for table in reversed(db.metadata.sorted_tables):
        db.session.query(table).delete()
    db.session.commit()
    return jsonify({"message": "Destroyed"})


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    username = get_jwt_identity()

    response = jsonify(msg="Logout successful")
    unset_jwt_cookies(response)

    return jsonify({"msg": "Successfully logged out"}), 200


@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(UPLOADFLOADER, filename)


if __name__ == "__main__":
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=APP_DEBUG)
