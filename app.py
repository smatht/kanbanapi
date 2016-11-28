#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
import datetime
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://matias:123456@ds147797.mlab.com:47797/kanbanapi')
mydb = client['kanbanapi']

tarjetas = [
]


##############################################################################
## Gets
##############################################################################
@app.route('/kanban/api/tarjetas', methods=['GET'])
def get_tarjetas():
    output = []
    for t in mydb.tarjetas.find():
        tarjeta = {
            "id": t['id'],
            "title": t['title'],
            "description": t['description'],
            "done": t['done']
        }
        output.append(tarjeta)
    return jsonify([make_public(tarjeta) for tarjeta in output])


@app.route('/kanban/api/tarjetas/<int:tarjeta_id>', methods=['GET'])
def get_tarjeta(tarjeta_id):
    pass
    t = mydb.tarjetas.find_one({'id': tarjeta_id})
    if t:
        tarjeta = {
            "id": t['id'],
            "title": t['title'],
            "description": t['description'],
            "done": t['done']
        }
    else:
        abort(404)

    return jsonify({'tarjeta': make_public(tarjeta)})


##############################################################################
## Posts
##############################################################################
@app.route('/kanban/api/tarjetas', methods=['POST'])
def create_tarjeta():
    if not request.json or not 'title' in request.json:
        abort(400)
    n = mydb.tarjetas.count()
    tarjeta = {
        "id": n + 1,
        "title": request.json['title'],
        "description": request.json.get('description', ""),
        "done": False
    }
    record = mydb.tarjetas.insert(tarjeta)
    print record
    # tarjetas.append(tarjeta)
    return jsonify({'estado': 'ok'}), 201


##############################################################################
## Puts
##############################################################################
@app.route('/kanban/api/tarjetas/<int:tarjeta_id>', methods=['PUT'])
def update_tarjeta(tarjeta_id):

    # tarjeta = [tarjeta for tarjeta in tarjetas if tarjeta['id'] == tarjeta_id]
    # if len(tarjeta) == 0:
    #     abort(404)
    if not request.json:
        abort(400)
    # if 'title' in request.json and type(request.json['title']) != unicode:
    #     abort(400)
    # if 'description' in request.json and type(request.json['description']) is not unicode:
    #     abort(400)
    # if 'done' in request.json and type(request.json['done']) is not bool:
    #     abort(400)
    tit = request.json.get('title');
    des = request.json.get('description')
    don = request.json.get('don')
    mydb.tarjetas.find_one_and_update({'id': tarjeta_id},
                                      {'$set': {'title': tit, 'description': des, 'done': don}})

    # tarjeta[0]['title'] = request.json.get('title', tarjeta[0]['title'])
    # tarjeta[0]['description'] = request.json.get('description', tarjeta[0]['description'])
    # tarjeta[0]['done'] = request.json.get('done', tarjeta[0]['done'])
    return jsonify({'estado': 'ok'})



##############################################################################
## Deletes
##############################################################################
@app.route('/kanban/api/tarjetas/<int:tarjeta_id>', methods=['DELETE'])
def delete_tarjeta(tarjeta_id):
    # tarjeta = [tarjeta for tarjeta in tarjetas if tarjeta['id'] == tarjeta_id]
    # if len(tarjeta) == 0:
    #     abort(404)
    # tarjetas.remove(tarjeta[0])
    mydb.tarjetas.delete_one({'id': tarjeta_id})
    return jsonify({'result': True})


##############################################################################
## Otros
##############################################################################
def make_public(tarjeta):
    nueva_tarjeta = {}
    for field in tarjeta:
        if field == 'id':
            nueva_tarjeta['uri'] = url_for('get_tarjeta', tarjeta_id=tarjeta['id'], _external=True)
        else:
            nueva_tarjeta[field] = tarjeta[field]
    return nueva_tarjeta


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Tarjeta no encontrada'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
