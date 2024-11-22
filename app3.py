from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email
import json



app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure random key



# Form definition using Flask-WTF
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')





@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()

    if form.validate_on_submit():  # Validates the form on POST
        # Collect all form data into a dictionary
        form_data = {
            "name": form.name.data,
            "email": form.email.data,
            "message": form.message.data,
        }

        # Redirect and send the dictionary as a JSON string
        return redirect(url_for('confirmation', form_data=json.dumps(form_data)))
    
    return render_template('index.html', form=form)



@app.route('/confirmation')
def confirmation():
    # Retrieve JSON string from the query parameter
    form_data = request.args.get('form_data', '{}')
    form_data = json.loads(form_data)  # Parse JSON string back to dictionary
    return render_template('confirmation.html', form_data=form_data)





if __name__ == '__main__':
    app.run(port=5003)