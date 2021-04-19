import flask
from flask import jsonify
from . import db_session
from .compositions import Composition

blueprint = flask.Blueprint('composition_api', __name__, template_folder='templates')

@blueprint.route('/api/compositions')
def get_composition():
    db_sess = db_session.create_session()
    composition = db_sess.query(Composition).all()
    l1 = []
    for item in composition:
        l1.append(item.to_dict(only=('Name', 'Autor')))
    return jsonify(
        {
            'compositions': l1
        }
    )