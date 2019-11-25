#!flask/bin/python
import six
from flask import Flask, jsonify, abort, request, make_response, url_for
import json

app = Flask(__name__, static_url_path="")

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


tarefas = [
    {
        'id': 1,
        'titulo': u'Testar API1',
        'descricao': u'Rodar codigo flask'
    },
    {
        'id': 2,
        'titulo': u'Pesquisa H4',
        'descricao': u'Pesquisar perguntas do relatorio e responde-las'
    }
]


def adicionaTarefa(tarefa):
    nova_tarefa = {}
    for i in tarefa:
        if i == 'id':
            nova_tarefa['uri'] = url_for('selecinaTarefa', tarefa_id=tarefa['id'],_external=True)
        else:
            nova_tarefa[i] = tarefa[i]
    return nova_tarefa


@app.route('/Tarefa', methods=['GET'])
def selecinaTarefas():
    return jsonify({'tarefas': [adicionaTarefa(tarefa) for tarefa in tarefas]})


@app.route('/Tarefa/<int:tarefa_id>', methods=['GET'])
def selecinaTarefa(tarefa_id):
    tarefa = [tarefa for tarefa in tarefas if tarefa['id'] == tarefa_id]
    if len(tarefa) == 0:
        abort(404)
    return jsonify({'tarefa': adicionaTarefa(tarefa[0])})


@app.route('/Tarefa', methods=['POST'])
def criaTarefa():
    values = request.get_json(force=True)
    print(values)
    if not request.json or 'titulo' not in request.json:
        abort(400)
    tarefa = {
        'id': tarefas[-1]['id'] + 1 if len(tarefas) > 0 else 1,
        'titulo': request.json['titulo'],
        'descricao': request.json.get('descricao', "")
    }
    tarefas.append(tarefa)
    return jsonify({'tarefa': adicionaTarefa(tarefa)}), 201


@app.route('/Tarefa/<int:tarefa_id>', methods=['PUT'])
def atualizaTarefa(tarefa_id):
    req = request.get_json(force=True)
    tarefa = [tarefa for tarefa in tarefas if tarefa['id'] == tarefa_id]
    #print(tarefa)
    #print(request.get_json(force=True))
    if len(tarefa) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'titulo' in request.json and \
            not isinstance(request.json['titulo'], six.string_types):
        abort(400)
    if 'descricao' in request.json and \
            not isinstance(request.json['descricao'], six.string_types):
        abort(400)
    tarefa[0]['titulo'] = request.json.get('titulo', tarefa[0]['titulo'])
    tarefa[0]['descricao'] = request.json.get('descricao',tarefa[0]['descricao'])
    return jsonify({'tarefa': adicionaTarefa(tarefa[0])})


@app.route('/Tarefa/<int:tarefa_id>', methods=['DELETE'])
def deletaTarefa(tarefa_id):
    tarefa = [tarefa for tarefa in tarefas if tarefa['id'] == tarefa_id]
    if len(tarefa) == 0:
        abort(404)
    tarefas.remove(tarefa[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
