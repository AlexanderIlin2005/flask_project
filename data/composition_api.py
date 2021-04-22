import flask
from flask import jsonify
from . import db_session
from .compositions import Composition

blueprint = flask.Blueprint('composition_api', __name__, template_folder='templates')

@blueprint.route('/api/compositions')
def get_all_compositions():
    db_sess = db_session.create_session()
    composition = db_sess.query(Composition).all()
    l1 = []
    for item in composition:
        l1.append(item.to_dict(only=('Name', 'Author')))
    return jsonify(
        {
            'compositions': l1
        }
    )


@blueprint.route('/api/<name>')
def get_one_composition(name):
    db_sess = db_session.create_session()
    composition = db_sess.query(Composition).filter(Composition.Name == name).one()
    return jsonify(
        {
            'composition': composition.to_dict()
        }
    )
