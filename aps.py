#!flask/bin/python
import six
from flask import Flask, jsonify, abort, request, make_response, url_for
import json
#from flaskext.mysql import MySQL
import pymysql
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

app = Flask(__name__, static_url_path="")
#mysql = MySQL()

#MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="rachelpbm",
  passwd="adgjlra1",
  database="projeto",
  charset="ascii"
)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/Tarefa', methods=['GET'])
def selecinaTarefas():
    mycursor = mydb.cursor()
    sql = "SELECT * FROM tarefa"
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    resp = jsonify(rows)
    return resp

@app.route('/Tarefa/<int:tarefa_id>', methods=['GET'])
def selecinaTarefa(tarefa_id):
    mycursor = mydb.cursor(prepared=True)
    print("Tarefa id: ",type(tarefa_id))
    sql = "SELECT * FROM tarefa WHERE id="+str(tarefa_id)
    print(sql)
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    print(json.dumps(rows))
    resp = jsonify(rows)
    print(resp)
    return resp


@app.route('/Tarefa', methods=['POST'])
def criaTarefa():
    values = request.get_json(force=True)
    print(values)
    if not request.json or 'titulo' not in request.json:
        abort(400)
    _titulo = request.json['titulo']
    _descricao = request.json.get('descricao', "")
    mycursor = mydb.cursor()
    sql = "INSERT INTO tarefa(titulo, descricao) VALUES(%s, %s)"
    data = (_titulo, _descricao)
    mycursor.execute(sql, data)
    mydb.commit()
    resp.status_code = 200
    print(mycursor.rowcount,"Tarefa adicionada")
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
    mycursor = mydb.cursor()
    sql = "UPDATE tarefa SET(titulo, descricao) VALUES(%s, %s)"
    data = (_titulo, _descricao)
    mycursor.execute(sql, data)
    mydb.commit()
    resp.status_code = 200
    print(mycursor.rowcount, "Tarefa atualizada")
    return resp


@app.route('/Tarefa/<int:tarefa_id>', methods=['DELETE'])
def deletaTarefa(tarefa_id):
    mycursor = mydb.cursor()
    mycursor.execute("DELETE * FROM tarefa WHERE id=%s",tarefa_id)
    rows = cursor.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    cursor.close() 
    conn.close()
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
