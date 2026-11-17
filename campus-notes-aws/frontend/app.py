"""Hospital Management System - Module 1: Patient Registration
Run:  pip install flask   then   python app.py   ->  http://127.0.0.1:5000
"""
import re
import sqlite3
from flask import Flask, request, render_template_string, redirect, url_for

DB = "hms.db"
app = Flask(__name__)


# ---------------- Database ----------------
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT UNIQUE,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                mobile TEXT NOT NULL,
                address TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )""")


# ---------------- Validation (DHMS-9) ----------------
def validate_patient(name, age, gender, mobile, address):
    """Returns (errors_dict, cleaned_values)."""
    errors = {}
    name = (name or "").strip()
    mobile = (mobile or "").strip()
    address = (address or "").strip()

    if not name:
        errors["name"] = "Name is required."
    # Allow letters separated by a single space, apostrophe, hyphen or dot.
    # Repeated punctuation such as A----- or four consecutive apostrophes is invalid.
    elif len(name) < 2 or len(name) > 50 or not re.fullmatch(
            r"[A-Za-z]+(?:[ .'-][A-Za-z]+)*", name):
        errors["name"] = "Invalid Name, Enter correct name."

    # Check the text before int(): Python's int() accepts underscores such as 1_0.
    age_text = str(age).strip() if age is not None else ""
    if not re.fullmatch(r"-?[0-9]+", age_text):
        age_int = None
        errors["age"] = "Age must be a whole number."
    else:
        age_int = int(age_text)
        if age_int < 0 or age_int > 120:
            errors["age"] = "Age must be between 0 and 120."

    if gender not in ("Male", "Female", "Other"):
        errors["gender"] = "Please select a gender."

    if not re.fullmatch(r"[6-9][0-9]{9}", mobile):
        errors["mobile"] = "Mobile must be 10 digits and start with 6-9."

    if not address:
        errors["address"] = "Address is required."
    elif len(address) > 200:
        errors["address"] = "Address must be at most 200 characters."

    return errors, dict(name=name, age=age_int, gender=gender,
                        mobile=mobile, address=address)


def is_duplicate(db, name, mobile):
    row = db.execute(
        "SELECT 1 FROM patients WHERE lower(name)=lower(?) AND mobile=?",
        (name, mobile)).fetchone()
    return row is not None


# ---------------- Templates ----------------
from layout import BASE

REGISTER = BASE + """
<h3>Register New Patient</h3>
{% if duplicate %}<p class="err">A patient with this name and mobile number already exists.</p>{% endif %}
<form method="post" novalidate>
 <label>Name</label><input name="name" value="{{ v.get('name','') }}">
 <span class="err">{{ errors.get('name','') }}</span>
 <label>Age</label><input name="age" value="{{ v.get('age','') }}">
 <span class="err">{{ errors.get('age','') }}</span>
 <label>Gender</label>
 <select name="gender">
  <option value="">-- select --</option>
  {% for g in ['Male','Female','Other'] %}
  <option {{ 'selected' if v.get('gender')==g }}>{{ g }}</option>{% endfor %}
 </select><span class="err">{{ errors.get('gender','') }}</span>
 <label>Mobile</label><input name="mobile" value="{{ v.get('mobile','') }}">
 <span class="err">{{ errors.get('mobile','') }}</span>
 <label>Address</label><textarea name="address" rows="3">{{ v.get('address','') }}</textarea>
 <span class="err">{{ errors.get('address','') }}</span>
 <button type="submit">Register</button>
</form>
"""

LIST = BASE + """
{% if new_id %}<p class="ok">Patient registered successfully. Patient ID: <b>{{ new_id }}</b></p>{% endif %}
<h3>Patients</h3>
<form method="get"><input name="q" placeholder="Search by ID, name or mobile" value="{{ q }}"
 style="width:70%"><button>Search</button></form>
<table><tr><th>Patient ID</th><th>Name</th><th>Age</th><th>Gender</th><th>Mobile</th><th>Address</th></tr>
{% for p in rows %}<tr><td>{{ p.patient_id }}</td><td>{{ p.name }}</td><td>{{ p.age }}</td>
<td>{{ p.gender }}</td><td>{{ p.mobile }}</td><td>{{ p.address }}</td></tr>
{% else %}<tr><td colspan="6">No patients found.</td></tr>{% endfor %}</table>
"""


# ---------------- Routes ----------------
@app.route("/")
def home():
    return redirect(url_for("patients"))


@app.route("/register", methods=["GET", "POST"])
def register():
    errors, values, duplicate = {}, {}, False
    if request.method == "POST":
        errors, values = validate_patient(
            request.form.get("name"), request.form.get("age"),
            request.form.get("gender"), request.form.get("mobile"),
            request.form.get("address"))
        if not errors:
            with get_db() as db:
                if is_duplicate(db, values["name"], values["mobile"]):
                    duplicate = True
                else:
                    # Save details and generate Patient ID (DHMS-10)
                    cur = db.execute(
                        "INSERT INTO patients (name,age,gender,mobile,address) "
                        "VALUES (?,?,?,?,?)",
                        (values["name"], values["age"], values["gender"],
                         values["mobile"], values["address"]))
                    pid = "P%04d" % cur.lastrowid
                    db.execute("UPDATE patients SET patient_id=? WHERE id=?",
                               (pid, cur.lastrowid))
                    return redirect(url_for("patients", new_id=pid))
        values = request.form
    return render_template_string(REGISTER, errors=errors, v=values,
                                  duplicate=duplicate)


@app.route("/patients")
def patients():
    q = (request.args.get("q") or "").strip()
    with get_db() as db:
        if q:
            like = f"%{q}%"
            rows = db.execute(
                "SELECT * FROM patients WHERE patient_id LIKE ? OR name LIKE ? "
                "OR mobile LIKE ? ORDER BY id DESC", (like, like, like)).fetchall()
        else:
            rows = db.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()
    return render_template_string(LIST, rows=rows, q=q,
                                  new_id=request.args.get("new_id"))


from appointments import bp as appointments_bp, init_appointments_db
app.register_blueprint(appointments_bp)

if __name__ == "__main__":
    init_db()
    init_appointments_db()
    app.run(debug=True)
