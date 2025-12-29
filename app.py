from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)

# CONFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus_v3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='dasjit62914@gmail.com', 
    MAIL_PASSWORD='Dasjit51987@'      
)

db = SQLAlchemy(app)
mail = Mail(app)

# MODELS
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) # Room, Lab, Equipment
    capacity = db.Column(db.Integer) 
    requirements = db.Column(db.Text) 

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(120), nullable=False)
    user_role = db.Column(db.String(20), nullable=False) # Teacher or Student
    reason = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

with app.app_context():
    db.create_all()
    if not Resource.query.first():
        db.session.add_all([
            Resource(name="Main Seminar Hall(D Block)", type="Room", capacity=150, requirements="AC, Projector"),
            Resource(name="FCS Lab 1", type="Lab", capacity=30, requirements="Linux, Python Environment"),
            Resource(name="Central Library (E block)", type="Lab", capacity=100, requirements="Quiet Zone, WiFi"),
            Resource(name="Smart Classroom (Admin Block)", type="Room", capacity=60, requirements="Smart Board"),
            Resource(name="AC class room", type="Room", capacity=50, requirements="White Board,fan"),
            Resource(name="Mini Seminar Hall(B Block)", type="Room", capacity=50, requirements="AC, Smart Board"),
            Resource(name="Chemistry lab(for 1st year student)", type="Lab", capacity=30, requirements="Basic Instruments"),

        ])
        db.session.commit()
        

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/resources')
def get_resources():
    res = Resource.query.all()
    return jsonify([{"id": r.id, "name": r.name, "type": r.type, "capacity": r.capacity, "requirements": r.requirements} for r in res])

@app.route('/api/book', methods=['POST'])
def book_resource():
    data = request.json
    start = datetime.fromisoformat(data['start_time'])
    end = datetime.fromisoformat(data['end_time'])
    
    # Conflict Resolution Logic [cite: 144]
    conflict = Booking.query.filter(
        Booking.resource_id == data['resource_id'],
        Booking.start_time < end,
        Booking.end_time > start
    ).first()
    
    if conflict:
        return jsonify({"message": "Error: Time slot occupied!"}), 400
    
    new_booking = Booking(
        resource_id=data['resource_id'],
        user_name=data['user_name'],
        user_email=data['email'],
        user_role=data['user_role'],
        reason=data.get('reason', ''),
        start_time=start,
        end_time=end
    )
    db.session.add(new_booking)
    db.session.commit()

    
    try:
        res_info = Resource.query.get(data['resource_id'])
        msg = Message("Campus Booking Success", sender=app.config['MAIL_USERNAME'], recipients=[data['email']])
        msg.body = f"Success! {res_info.name} is booked for {data['user_name']} ({data['user_role']})."
        mail.send(msg)
    except: pass

    return jsonify({"message": "Booking successful! Confirmation sent."})
if __name__ == '__main__':
    # Get port from environment, default to 5000 if not found
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
@app.route('/', methods=['GET', 'HEAD'])
def home():
    return render_template('index.html')
