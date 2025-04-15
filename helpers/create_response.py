from flask_pydantic import ValidationError
from werkzeug.exceptions import NotFound, BadRequest, Conflict, Forbidden
from flask import jsonify
from helpers import exceptions
from helpers.exceptions import IncorrectData
from flask_jwt_extended.exceptions import JWTDecodeError
import jwt


def get_first_error(e):
    errors = []

    if e.form_params:
        errors += e.form_params

    if e.query_params:
        errors += e.query_params

    if e.body_params:
        errors += e.body_params

    if e.path_params:
        errors += e.path_params

    error = errors[0]
    return f"{error['msg']}: {error['loc']}"


def creates_response(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            print(get_first_error(e))
            return jsonify({"Validation error": f"{get_first_error(e)}"}), 400
        except ValueError as e:
            return jsonify({"Validation error": f"{str(e)}"}), 400
        except BadRequest as e:
            return jsonify({"reason": "cant parse request"}), 400
        except Forbidden as e:
            return jsonify({"reason": "not access"}), 403
        except NotFound as e:
            return jsonify({"reason": "object not found"}), 404
        except Conflict as e:
            return jsonify({"reason": "conflict"}), 409
        except IncorrectData as e:
            return jsonify({"reason": "incorrect data"}), 401
        except JWTDecodeError as e:
            return jsonify({"reason": "Incorrect token"}), 403
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({"reason": "Signature verification failed"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 422
        except Exception as e:
            print(e)
            return jsonify({"reason": "server error "+str(e)}), 500

    wrapper.__name__ = func.__name__
    return wrapper
