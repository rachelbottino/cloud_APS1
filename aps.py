#!flask/bin/python
import six
from flask import Flask, jsonify, abort, request, make_response, url_for
import json
from flaskext.mysql import MySQL
import pymysql

app = Flask(__name__, static_url_path="")
mysql = MySQL()

#MySQL
app.config['MYSQL_DATABASE_DB'] = 'projeto'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/Tarefa', methods=['GET'])
def selecinaTarefas():
    sql = "SELECT * FROM tarefa"
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    resp = jsonify(rows)
    res.status_code = 200
    cursor.close()
    conn.close()
    return resp

@app.route('/Tarefa/<int:tarefa_id>', methods=['GET'])
def selecinaTarefa(tarefa_id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM tarefa WHERE id = %s",tarefa_id)
    rows = cursor.fetchall()
    resp = jsonify(rows)
    res.status_code = 200
    cursor.close()
    conn.close()
    return resp


@app.route('/Tarefa', methods=['POST'])
def criaTarefa():
    values = request.get_json(force=True)
    print(values)
    if not request.json or 'titulo' not in request.json:
        abort(400)
    _titulo = request.json['titulo']
    _descricao = request.json.get('descricao', "")
    sql = "INSERT INTO tarefa(titulo, descricao) VALUES(%s, %s)"
    data = (_titulo, _descricao)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()
    resp.status_code = 200
    cursor.close() 
    conn.close()
    print("Tarefa adicionada")
    return resp

@app.route('/Tarefa/<int:tarefa_id>', methods=['PUT'])
def atualizaTarefa(tarefa_id):
    req = request.get_json(force=True)
    if not request.json:
        abort(400)
    if 'titulo' in request.json and \
            not isinstance(request.json['titulo'], six.string_types):
        abort(400)
    if 'descricao' in request.json and \
            not isinstance(request.json['descricao'], six.string_types):
        abort(400)
    _titulo = request.json['titulo']
    _descricao = request.json.get('descricao', "")
    sql = "UPDATE tarefa SET(titulo, descricao) VALUES(%s, %s)"
    data = (_titulo, _descricao)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()
    resp.status_code = 200
    cursor.close() 
    conn.close()
    print("Tarefa adicionada")
    return resp


@app.route('/Tarefa/<int:tarefa_id>', methods=['DELETE'])
def deletaTarefa(tarefa_id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("DELETE * FROM tarefa WHERE id=%s",tarefa_id)
    rows = cursor.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    cursor.close() 
    conn.close()
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
