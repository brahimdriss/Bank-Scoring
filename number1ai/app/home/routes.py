# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""
from flask import jsonify, render_template, redirect, request, url_for
from app.home import blueprint
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.base.forms import CreateClassifyForm
from app import login_manager
from jinja2 import TemplateNotFound
import pandas as pd
import dash
import dash_html_components as html
from Dashboard import Dash_App1, Dash_App2
from sklearn.externals import joblib
import pickle

@blueprint.route('/index')
@login_required
def index():


    return render_template('index.html', dash_url=Dash_App1.url_base)
    #return render_template('index.html')



@blueprint.route('/<template>', methods=["GET","POST"])
def route_template(template):

    if not current_user.is_authenticated:
        return redirect(url_for('base_blueprint.login'))


    if template=="ui-tables":
        df = pd.read_csv("ger_data.csv")
        return render_template("ui-tables.html", df_view=df)
        # return render_template(template + '.html')

        
    if template=="ui-notifications":
        return render_template('ui-notifications.html', dash_url=Dash_App2.url_base)

    if template == "ui-icons":
        create_classify_form = CreateClassifyForm(request.form)
        if 'create_classify' in request.form:

            def replaceWord(word, cible, racine):
                return cible[racine.index(word)]

            df = pd.read_csv("ger_data.csv")
            mean_age, std_age = df["Age"].mean(), df["Age"].std()
            mean_duration, std_duration = df["Duration"].mean(), df["Duration"].std()
            mean_cred, std_cred = df["Credit_Amount"].mean(), df["Credit_Amount"].std()




            
            Status_Account = request.form['Status_Account']
            Status_Account = replaceWord(Status_Account, ["A11", "A12", "A13", "A14"]
                                                       ,["< 0 DM", "0 <= ... <  200 DM", ">= 200 DM ", "no checking account"])

            
            Credit_History = request.form['Credit_History']
            Credit_History= replaceWord(Credit_History, ['A30', 'A31', 'A32', 'A33', 'A34'], ['No credits taken', 'All credits at this bank paid back duly',
                                                                             'Existing credits paid back duly till now', 'Delay in paying off in the past', 'Critical account'])
            

            Saving_Account = request.form['Saving_Account']
            Saving_Account = replaceWord(Saving_Account,
                                                         ['A61', 'A62', 'A63', 'A64', 'A65'],
                                                         ['< 100 DM', '100 <= ... <500 DM', '500<= ... < 1000', '>= 1000', 'Unknown / No Saving Account'])



            Present = request.form['Present']
            Present = replaceWord(Present,
                                                  ['A71', 'A72', 'A73', 'A74', 'A75'],
                                                  ['Unemployed', '< 1 Year', '100<= ... <4 Years', '4<= ... <7 Years', '>= 7 Years'])


            Property = request.form['Property']
            Property = replaceWord(Property,
                                                   ['A121', 'A122', 'A123', 'A124'],
                                                   ['Real Estate', 'building society savings agreement/life insurance', 'car or other', 'Unknown/No Property'])
            
            
            
            Other_Installment = request.form['Other_Installment']
            Other_Installment = replaceWord(Other_Installment,
                                                            ['A141', 'A142', 'A143'],
                                                            ['Bank', 'Stores', 'None'])


            Housing = request.form['Housing']
            Housing = replaceWord(Housing,
                                                  ['A151', 'A152', 'A153'],
                                                  ['Rent', 'Own', 'For Free'])


            Foreign_Worker = request.form['Foreign_Worker']
            Foreign_Worker = replaceWord(Foreign_Worker,
                              ['A201', 'A202'],
                              ['Yes', 'No'])

            
            Age = request.form['Age']
            Age = int(Age)
            Age = Age* std_age + mean_age
            

           
            Duration = request.form['Duration']
            Duration = int(Duration)
            Duration = Duration * std_duration + mean_duration
             


            Credit_Amount = request.form['Credit_Amount']
            Credit_Amount = int(Credit_Amount)
            Credit_Amount = Credit_Amount*std_cred + mean_cred

            inpt = [Status_Account, Duration, Credit_History, Credit_Amount, Saving_Account,
                    Present, Property, Age, Other_Installment, Housing, Foreign_Worker]
            
            
            df_inpt = pd.DataFrame([inpt], columns=['Status_Account', 'Duration', 'Credit_History', 'Credit_Amount',
       'Saving_Account', 'Present', 'Property', 'Age', 'Other_Installment',
       'Housing', 'Foreign_Worker'])

            pred_num = df_inpt[['Duration','Credit_Amount','Age']]
            
            
            liste= []
            inpt_cat = df_inpt.select_dtypes(include=['object'])

            with open('dictEnc.pickle', 'rb') as handle:
                dictEnc = pickle.load(handle)

            for col in inpt_cat.columns:
                le = dictEnc[col]
                var = le.transform(df_inpt[col])
                liste.append(pd.DataFrame(var)) 

            data_cat_LE = pd.concat(liste, axis=1)
            ohe = dictEnc['onehot']
            oneHotedToPredict = ohe.transform(data_cat_LE)
            df_pred = pd.DataFrame(oneHotedToPredict.toarray())
            

            data_to_pred = pd.concat([pred_num ,df_pred],axis=1)

            xgb_ger = joblib.load('xgb_germany_88_new.pkl')

            prediction = xgb_ger.predict(data_to_pred)

            if prediction == 0:
                prediction = "Bad Client"
            else :
                prediction = "Good Client"


            """


            # Load the model from the file
            

            # Use the loaded model to make predictions
            knn_from_joblib.predict(X_test)
            """

            # user = User.query.filter_by(username=username).first()
            # if user:
            #     return render_template('login/register.html', msg='Username already registered', form=create_account_form)
            # user = User.query.filter_by(email=email).first()
            # if user:
            #     return render_template('login/register.html', msg='Email already registered', form=create_account_form)
            # # else we can create the user
            # user = User(**request.form)
            # db.session.add(user)
            # db.session.commit()
            return render_template('ui-icons.html', msg=" Prediction realised with precision = 88% ", form=create_classify_form, pred=prediction)
        else:
            return render_template('ui-icons.html', form=create_classify_form)
      

    
      # return render_template(template + '.html')
    try:
        return render_template(template + '.html')

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500




