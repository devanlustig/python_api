from flask import Flask, jsonify, request, make_response, Response
from flask_httpauth import HTTPBasicAuth
from model import Karyawan
from collections import OrderedDict
import json

app = Flask(__name__)
app.config["DEBUG"] = True
auth = HTTPBasicAuth()

users = {
    "admin": "Admin12345"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username


@app.route('/karyawan', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth.login_required
def karyawan():
    try:
        dt = Karyawan()
        data = []

        if request.method == 'GET':
            id_ = request.args.get("id")
            if id_:
                query = "SELECT * FROM data_karyawan WHERE id = %s ORDER BY id DESC"
                values = (id_,)
            else:
                query = "SELECT * FROM data_karyawan ORDER BY id DESC"
                values = None
            data = dt.get_data(query, values)

            formatted_data = []
            for row in data:
                formatted_data.append(OrderedDict([
                    ("id", row["id"]),
                    ("nama", row["nama"]),
                    ("alamat", row["alamat"])
                ]))
            return Response(json.dumps({"data": formatted_data}, ensure_ascii=False),content_type="application/json")

        elif request.method == 'POST':
            datainput = request.json
            nama = datainput['nama']
            alamat = datainput['alamat']

            query = "INSERT INTO data_karyawan (nama, alamat) VALUES (%s, %s)"
            values = (nama, alamat)
            dt.insert_data(query, values)
            data = [{'pesan': 'data berhasil ditambah'}]

        elif request.method == 'PUT':
            datainput = request.json
            id_ = datainput.get('id')
            if id_ is None:
                            return make_response(jsonify({'error': 'Parameter id tidak diberikan'}), 400)

            query = "UPDATE data_karyawan SET"
            values = []

            if 'nama' in datainput:
                nama = datainput['nama']
                query += " nama = %s,"
                values.append(nama)
            if 'alamat' in datainput:
                alamat = datainput['alamat']
                query += " alamat = %s,"
                values.append(alamat)

            query = query.rstrip(',') + " WHERE id = %s"
            values.append(id_)
            dt.insert_data(query, tuple(values))
            data = [{'pesan': 'berhasil mengubah data'}]

        elif request.method == 'DELETE':
            id_ = request.args.get("id")
            if id_:
                query = "DELETE FROM data_karyawan WHERE id = %s"
                values = (id_,)
                dt.execute_query(query, values)
                data = [{'pesan': 'data berhasil dihapus'}]
            else:
                return make_response(jsonify({'error': 'Parameter id tidak diberikan'}), 400)
        else:
            return make_response(jsonify({'error': 'Metode HTTP tidak didukung'}), 405)

    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 400)   
    return make_response(jsonify({'data': data}), 200)

if __name__ == '__main__':
    app.run()
