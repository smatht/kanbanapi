#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
import datetime
from pymongo import MongoClient
import pymongo

app = Flask(__name__)

client = MongoClient('mongodb://matias:123456@ds111798.mlab.com:11798/encuesta')
mydb = client['encuesta']

preguntas = [
]

##############################################################################
## Gets
##############################################################################
@app.route('/encuesta/api/preguntas', methods=['GET'])
def get_preguntas():
    output = []
    for t in mydb.questions.find().sort("id"):
        pregunta = {
            "id": t['id'],
            "question": t['question'],
            "posible_answers": t['posible_answers']
        }
        output.append(pregunta)
    return jsonify({'questions': output})


@app.route('/encuesta/api/encuestas', methods=['GET'])
def get_encuestas():
    output = []
    for t in mydb.quiz.find().sort("id", pymongo.DESCENDING):
        encuesta = {
            "id": t['id'],
            "nombre_encuestador": t['nombre_encuestador'],
            "mail_encuestador": t['mail_encuestador'],
            "nombre_encuestado": t['nombre_encuestado'],
            "ciudad": t['ciudad'],
            "sexo": t['sexo'],
            "edad": t['edad'],
            "respuestas":t['respuestas']
        }
        output.append(encuesta)
    return jsonify({'quiz': output})


# @app.route('/kanban/api/tarjetas/<int:tarjeta_id>', methods=['GET'])
# def get_tarjeta(tarjeta_id):
#     pass
#     t = mydb.tarjetas.find_one({'id': tarjeta_id})
#     if t:
#         tarjeta = {
#             "id": t['id'],
#             "title": t['title'],
#             "description": t['description'],
#             "done": t['done']
#         }
#     else:
#         abort(404)

#     return jsonify({'tarjeta': make_public(tarjeta)})


##############################################################################
## Posts
##############################################################################
# @app.route('/kanban/api/tarjetas', methods=['POST'])
# def create_tarjeta():
#     if not request.json or not 'title' in request.json:
#         abort(400)
#     n = mydb.tarjetas.count()
#     tarjeta = {
#         "id": n + 1,
#         "title": request.json['title'],
#         "description": request.json.get('description', ""),
#         "done": False
#     }
#     record = mydb.tarjetas.insert(tarjeta)
#     print record
#     # tarjetas.append(tarjeta)
#     return jsonify({'estado': 'ok'}), 201


##############################################################################
## Puts
##############################################################################
# @app.route('/kanban/api/tarjetas/<int:tarjeta_id>', methods=['PUT'])
# def update_tarjeta(tarjeta_id):

#     if not request.json:
#         abort(400)
    
#     tit = request.json.get('title');
#     des = request.json.get('description')
#     don = request.json.get('don')
#     mydb.tarjetas.find_one_and_update({'id': tarjeta_id},
#                                       {'$set': {'title': tit, 'description': des, 'done': don}})

    
#     return jsonify({'estado': 'ok'})



##############################################################################
## Deletes
##############################################################################
# @app.route('/kanban/api/tarjetas/<int:tarjeta_id>', methods=['DELETE'])
# def delete_tarjeta(tarjeta_id):
#     mydb.tarjetas.delete_one({'id': tarjeta_id})
#     return jsonify({'result': True})


##############################################################################
## Otros
##############################################################################
# def make_public(tarjeta):
#     nueva_tarjeta = {}
#     for field in tarjeta:
#         if field == 'id':
#             nueva_tarjeta['uri'] = url_for('get_tarjeta', tarjeta_id=tarjeta['id'], _external=True)
#         else:
#             nueva_tarjeta[field] = tarjeta[field]
#     return nueva_tarjeta


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Consulta no manejada'}), 404)


if __name__ == '__main__':
    app.run(debug=True)