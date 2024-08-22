import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Patient_details(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    gender = db.Column(db.Text)
    state = db.Column(db.Text)
    phn_no = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    age = db.Column(db.Integer)
    blood_group = db.Column(db.Text)
    fathers_name = db.Column(db.Text)
    can_view_records = db.Column(db.Boolean, default=True, nullable=False,server_default='1')  # This column controls visibility
    
    def __init__(self, name, gender, state, phn_no, weight, age, blood_group, fathers_name):
        self.name = name
        self.gender = gender
        self.state = state
        self.phn_no = phn_no
        self.weight = weight
        self.age = age
        self.blood_group = blood_group
        self.fathers_name = fathers_name

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/addpatient', methods=['GET', 'POST'])
def addpatient():
    if request.method == "POST":
        name = request.form.get('name')
        gender = request.form.get('gender')
        state = request.form.get('state')
        phn_no = request.form.get('phn_no')
        weight = request.form.get('weight')
        age = request.form.get('age')
        blood = request.form.get('blood')
        f_name = request.form.get('f_name')
        new_patient = Patient_details(name=name, gender=gender, state=state, phn_no=phn_no, weight=weight, age=age, blood_group=blood, fathers_name=f_name)
        db.session.add(new_patient)     
        db.session.commit()
        flash(f"{name} added successfully!!!")
        return redirect(url_for('addpatient'))
    return render_template('addpatient.html')

@app.route('/queue')
def queue():
    # Only show patients who haven't been marked as done
    all_patients = Patient_details.query.filter_by(can_view_records=True).all()
    total_patients = len(all_patients)
    return render_template('queue.html', all_patients=all_patients, total_patients=total_patients)

@app.route('/delete_patient/<int:id>')
def delete_patient(id):
    patient = Patient_details.query.get_or_404(id) 
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('queue'))

@app.route('/reschedule_patient/<int:id>', methods=['POST'])
def reschedule_patient(id):
    patient_to_reschedule = Patient_details.query.get_or_404(id)

    # Delete the current patient entry
    db.session.delete(patient_to_reschedule)
    db.session.commit()

    # Re-create the patient entry (mimicking "rescheduling")
    new_patient = Patient_details(
        name=patient_to_reschedule.name,
        gender=patient_to_reschedule.gender,
        state=patient_to_reschedule.state,
        phn_no=patient_to_reschedule.phn_no,
        weight=patient_to_reschedule.weight,
        age=patient_to_reschedule.age,
        blood_group=patient_to_reschedule.blood_group,
        fathers_name=patient_to_reschedule.fathers_name
    )
    db.session.add(new_patient)
    db.session.commit()

    flash(f"Patient {new_patient.name} has been rescheduled to the end of the queue.")
    return redirect(url_for('queue'))

@app.route('/mark_done/<int:id>', methods=['POST'])
def mark_done(id):
    patient = Patient_details.query.get_or_404(id)
    patient.can_view_records = False  # Mark the record as done (hidden from the list)
    db.session.commit()
    return redirect(url_for('queue'))  # Redirect back to the queue view

if __name__ == "__main__":
    app.run(debug=True)
