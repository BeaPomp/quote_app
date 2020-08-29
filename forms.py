from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, validators

class Form_update(FlaskForm):
    name = StringField("Name:", [validators.Length(min = 3, max = 20)])
    surname = StringField("Surname:",[validators.Length(min = 3, max = 20)] )
    quote = TextAreaField("Quote:",[validators.Length(min = 3, max = 200)])
    submit = SubmitField("Update")

class Form_add(FlaskForm):
    image = StringField("Image:", [validators.DataRequired()])
    bio = TextAreaField("Biography:", [validators.Length(min = 3, max = 400)])
    submit = SubmitField("Add")

class Form_registration(FlaskForm):
    username = StringField("Username:", [validators.DataRequired()])
    email = StringField("Email:", [validators.DataRequired(), validators.Email()]) 
    password = PasswordField("Password:", [validators.DataRequired()])
    password2 = PasswordField("Password:", [validators.DataRequired(), validators.EqualTo("password")])
    submit = SubmitField("Register") 

class Form_login(FlaskForm):
    email = StringField("Email:", [validators.DataRequired()])
    password = PasswordField("Password:", [validators.DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")