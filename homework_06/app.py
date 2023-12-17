from flask import Flask, render_template, request

from models import Record, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@db/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    records = Record.query.all()
    return render_template('index.html', records=records)


@app.route('/add', methods=['POST'])
def add_record():
    content = request.form.get('content')
    new_record = Record(content=content)
    db.session.add(new_record)
    db.session.commit()
    return redirect('/')
