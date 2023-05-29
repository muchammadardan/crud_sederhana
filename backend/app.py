from flask import Flask, request, jsonify, render_template
import mysql.connector
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
db = mysql.connector.connect(
    host="localhost", user="root", password="", database="miniapps", port=3300
)


# cursor = db.cursor()
# cursor.execute("select * from contacts")
# data = cursor.fetchall()
# print(data)
# @app.route("/")
# def index():
#     return render_template("../frontend/list.html")


# Menampilkan Data
@app.route("/contacts", methods=["GET"])
def get_contacts():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()
    result = []
    for contact in contacts:
        contact_data = {
            "id": contact[0],
            "fullname": contact[1],
            "phone": contact[2],
            "note": contact[3],
        }
        result.append(contact_data)
    return jsonify(result)


# Membuat data baru
@app.route("/contacts", methods=["POST"])
def create_contacts():
    data = request.get_json()
    fullname = data["fullname"]
    phone = data["phone"]
    note = data["note"]

    cursor = db.cursor()
    query = "INSERT INTO contacts (fullname, phone, note) VALUES (%s, %s, %s)"
    values = (fullname, phone, note)
    cursor.execute(query, values)
    db.commit()

    return jsonify({"message": "Contacts successfully created"})


# Mengambi data yang ada berdasarkan id
@app.route("/contacts/<int:contact_id>", methods=["GET"])
def get_contact(contact_id):
    cursor = db.cursor()
    query = "SELECT * FROM contacts WHERE id = %s"
    values = (contact_id,)
    cursor.execute(query, values)
    contact = cursor.fetchone()

    if contact:
        contact_data = {
            "id": contact[0],
            "fullname": contact[1],
            "phone": contact[2],
            "note": contact[3],
        }
        return jsonify(contact_data)

    else:
        return jsonify({"message": "Contact not found"})


# Mengupdate data Contact
@app.route("/contacts/<int:contact_id>", methods=["PUT"])
def update_contacts(contact_id):
    data = request.get_json()
    fullname = data["fullname"]
    phone = data["phone"]
    note = data["note"]

    cursor = db.cursor()
    query = "UPDATE contacts SET fullname = %s, phone = %s, note = %s WHERE id=%s"
    values = (fullname, phone, note, contact_id)
    cursor.execute(query, values)
    db.commit()

    return jsonify({"message": "Contact successfully update"})


# Menghapus data contacts
@app.route("/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contacts(contact_id):
    cursor = db.cursor()
    query = "DELETE FROM contacts WHERE id = %s"
    values = (contact_id,)
    cursor.execute(query, values)

    return jsonify({"message": "Contact successfully deleted"})


if __name__ == "__main__":
    app.run(debug=True)
