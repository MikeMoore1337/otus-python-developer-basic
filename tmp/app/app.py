from flask import Flask, render_template

from models import Record, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_database_user:your_database_password@db/your_database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/add_record/<content>')
def add_record(content):
    new_record = Record(content=content)
    db.session.add(new_record)
    db.session.commit()
    return 'Record added successfully!'


@app.route('/records')
def show_records():
    records = Record.query.all()
    return render_template('records.html', records=records)
