import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from collections import Counter

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''

    occupation = ['administrative_staff' , 'business_owner' , 'domestic_worker' , 'executive' , 'independent_worker' , 'jobless' , 'manual_worker' , 'retired_worker' , 'service_worker' , 'student' , 'technical_specialist' , 'unidentified']
    education_level = ['college' , 'elementary_school' , 'high_school' , 'unidentified']
    marital_status = ['divorced' , 'married' , 'single']
    communication_channel = ['landline' , 'mobile' , 'unidentified']
    call_month = ['April' , 'August' , 'December' , 'February' , 'January' , 'July' , 'June' , 'March' , 'May' , 'November' , 'October' , 'September']
    previous_campaign_outcome = ['other_outcome' , 'successful' , 'unidentified' , 'unsuccessful']


    arr = [occupation , [] , education_level , marital_status , communication_channel , call_month , [] , [] , [] , previous_campaign_outcome]


    int_features = [int(x) for x in request.form.values()]

    # ptr = 0
    # for x in request.form.values():
    #     if (ptr == 0 or (ptr >= 6 and ptr <= 8)):
    #         ptr += 1
    #         continue
    #     curx = 0
    #     for ele in arr[ptr]:
    #         if ele == x:
    #             int_features.append(curx)
    #             break
    #         curx += 1
    #     ptr += 1





    print(int_features)
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    # output = round(prediction[0], 2)

    print('THe prediction is' , prediction[0])

    ans = "converted"
    if prediction[0] == 1:
        ans = "Not converted"

    return render_template('index.html', prediction_text='Converted Status is $ {}'.format(ans))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


