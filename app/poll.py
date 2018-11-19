from flask import Flask, render_template, request, redirect, make_response
from flask_bootstrap import Bootstrap
import json


import datetime

app = Flask(__name__, static_url_path='/static')
Bootstrap(app)

fields = ['1', '2', '3', '4', '5']
topic1 = 'Line security & crypto (KPN)'
topic2 = 'Threat Hunting (ING CDC)'
topic3 = 'Live Hacking demo (FOX-IT)'
topic4 = 'Slice of Security'

filename = 'data.txt'
feedback_list = []


@app.route('/')
def root():
    return render_template('poll.html')


def getcookie():
    name = request.cookies.get('quest4dave')
    if name:
        return True
    else:
        return False


@app.route('/poll')
def poll():

    feedback = dict(request.args.items())

    if not getcookie():
        feedback_list.append(feedback)
        with open(filename, mode='w') as my_file:
            my_file.write(json.dumps(feedback_list) + "\n")
        response = make_response(redirect('/thankyou'))
        response.set_cookie('quest4dave', "banaan",
                            expires=datetime.datetime.now()
                            + datetime.timedelta(days=30))
        return response
    else:
        return redirect("/youalreadyvoted")


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


@app.route('/youalreadyvoted')
def alreadyvoted():
    return render_template('alreadyvoted.html')


@app.route('/results')
def show_results():
    votes = {}
    topic1_score = 0
    topic2_score = 0
    topic3_score = 0
    topic4_score = 0
    counter = 0
    for f in fields:
        votes[f] = 0

    with open(filename, 'r') as read_file:
        feedback_list = json.load(read_file)
    for feedback in feedback_list:
        topic1_score += int(feedback['topic1'])
        topic2_score += int(feedback['topic2'])
        topic3_score += int(feedback['topic3'])
        topic4_score += int(feedback['topic4'])
        counter += 1
    scores = [{'topic': topic1, 'score': topic1_score},
              {'topic': topic2, 'score': topic2_score},
              {'topic': topic3, 'score': topic3_score},
              {'topic': topic4, 'score': topic4_score}]

    return render_template('results.html', scores=scores, counter=counter)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
