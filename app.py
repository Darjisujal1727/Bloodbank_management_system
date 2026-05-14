from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime


APP_DATA_FILE = os.path.join(os.path.dirname(__file__), 'storage.json')


def _load_db():
    if not os.path.exists(APP_DATA_FILE):
        return {"donors": [], "donorIdCounter": 0}
    with open(APP_DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return {"donors": [], "donorIdCounter": 0}


def _save_db(data):
    with open(APP_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _next_donor_id(db):
    db['donorIdCounter'] = int(db.get('donorIdCounter') or 0) + 1
    return 'DNR' + str(db['donorIdCounter']).zfill(5)


def _public_donor(d):
    return {
        "donorId": d.get("donorId"),
        "name": d.get("name"),
        "contact_no": d.get("contact_no"),
        "age": d.get("age"),
        "gender": d.get("gender"),
        "address": d.get("address"),
        "blood_group": d.get("blood_group"),
        "disease": d.get("disease"),
        "email": d.get("email"),
        "createdAt": d.get("createdAt"),
        "last_donation": d.get("last_donation"),
        "next_eligibility": d.get("next_eligibility"),
        "status": d.get("status"),
    }


app = Flask(__name__)
CORS(app)


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"ok": True, "time": datetime.utcnow().isoformat() + 'Z'})


@app.route('/api/register', methods=['POST'])
def register():
    payload = request.get_json(silent=True) or {}
    required = ["name", "contact_no", "age", "gender", "address", "blood_group", "email", "password"]
    missing = [k for k in required if not payload.get(k)]
    if missing:
        return jsonify({"ok": False, "error": "Missing fields", "fields": missing}), 400

    db = _load_db()
    email = (payload.get('email') or '').strip().lower()
    if any((d.get('email') or '').lower() == email for d in db.get('donors', [])):
        return jsonify({"ok": False, "error": "Email already registered"}), 409

    donor = {
        "donorId": _next_donor_id(db),
        "name": payload.get('name') or '',
        "contact_no": payload.get('contact_no') or '',
        "age": payload.get('age') or '',
        "gender": payload.get('gender') or '',
        "address": payload.get('address') or '',
        "blood_group": payload.get('blood_group') or '',
        "disease": payload.get('disease') or '',
        "email": email,
        "password": payload.get('password') or '',
        "createdAt": datetime.utcnow().isoformat() + 'Z',
        "last_donation": None,
        "next_eligibility": None,
        "status": 'new'
    }
    db['donors'].append(donor)
    _save_db(db)
    return jsonify({"ok": True, "donor": _public_donor(donor)})


@app.route('/api/login', methods=['POST'])
def login():
    payload = request.get_json(silent=True) or {}
    email = (payload.get('email') or '').strip().lower()
    password = payload.get('password') or ''
    db = _load_db()
    match = next((d for d in db.get('donors', []) if (d.get('email') or '').lower() == email and (d.get('password') or '') == password), None)
    if not match:
        return jsonify({"ok": False, "error": "Invalid credentials"}), 401
    return jsonify({"ok": True, "donor": _public_donor(match)})


@app.route('/api/donor', methods=['GET'])
def donor_by_email():
    email = (request.args.get('email') or '').strip().lower()
    if not email:
        return jsonify({"ok": False, "error": "email query required"}), 400
    db = _load_db()
    match = next((d for d in db.get('donors', []) if (d.get('email') or '').lower() == email), None)
    if not match:
        return jsonify({"ok": False, "error": "Not found"}), 404
    return jsonify({"ok": True, "donor": _public_donor(match)})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    app.run(host='127.0.0.1', port=port, debug=True)


