from flask import Flask, redirect, render_template, request
from models import Record, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://myuser:mypassword@db/mydatabase"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key"

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/", endpoint="index")
def home():
    return render_template("index.html")


@app.route("/records/", methods=["GET", "POST"], endpoint="records")
def records():
    if request.method == "POST":
        content = request.form.get("content")
        new_record = Record(content=content)
        db.session.add(new_record)
        db.session.commit()
        return redirect("/records/")
    else:
        records = Record.query.all()
        return render_template("records.html", records=records)


@app.route("/view_records", methods=["GET", "POST"], endpoint="view_records")
def view_records():
    if request.method == "POST":
        record_id = request.form.get("record_id")
        record = Record.query.get(record_id)
        if record:
            db.session.delete(record)
            db.session.commit()

    records = Record.query.all()
    return render_template("view_records.html", records=records)


@app.route("/about/", endpoint="about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
