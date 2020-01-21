# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField,SelectField
from wtforms.validators import InputRequired, Email, DataRequired,Required

## login and registration

class LoginForm(FlaskForm):
    username = TextField    ('Username', id='username_login'   , validators=[DataRequired()])
    password = PasswordField('Password', id='pwd_login'        , validators=[DataRequired()])

class CreateAccountForm(FlaskForm):
    username = TextField('Username'     , id='username_create' , validators=[DataRequired()])
    email    = TextField('Email'        , id='email_create'    , validators=[DataRequired(), Email()])
    password = PasswordField('Password' , id='pwd_create'      , validators=[DataRequired()])


class CreateClassifyForm(FlaskForm):
    Status_Account = SelectField('Status_Account', id='status_account', choices=[(status, status) for status in ["< 0 DM", "0 <= ... <  200 DM", ">= 200 DM ", "no checking account"]], validators=[Required()])
    Duration = TextField('Duration', id='duration', validators=[DataRequired()])
    Credit_History = SelectField('Credit_History', id='credit_history', choices=[(status, status) for status in ['No credits taken', 'All credits at this bank paid back duly',
                                                                                                               'Existing credits paid back duly till now', 'Delay in paying off in the past', 'Critical account']], validators=[Required()])
    
    Credit_Amount = TextField('Credit_Amount', id='credit_amount', validators=[DataRequired()])
    
    Saving_Account = SelectField('Saving_Account', id='saving_account', choices=[(status, status) for status in [
                               '< 100 DM', '100 <= ... <500 DM', '500<= ... < 1000', '>= 1000', 'Unknown / No Saving Account']], validators=[Required()])

    Present = SelectField('Present', id='present', choices=[(status, status) for status in [
                          'Unemployed', '< 1 Year', '100<= ... <4 Years', '4<= ... <7 Years', '>= 7 Years']], validators=[Required()])
    Property = SelectField('Property', id='property', choices=[(status, status) for status in [
                           'Real Estate', 'building society savings agreement/life insurance', 'car or other', 'Unknown/No Property']], validators=[Required()])
    Age = TextField('Age', id='age', validators=[DataRequired()])
    Other_Installment = SelectField('Other_Installment', id='other_install', choices=[(
        status, status) for status in ['Bank', 'Stores', 'None']], validators=[Required()])
    Housing = SelectField('Housing', id='housing', choices=[(status, status) for status in [
                          'Rent', 'Own', 'For Free']], validators=[Required()])
    Foreign_Worker = SelectField('Foreign_Worker', id='foreign_worker', choices=[
                                 (status, status) for status in ['Yes', 'No']], validators=[Required()])

