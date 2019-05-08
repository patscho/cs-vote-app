from flask import Flask, render_template, request, redirect, make_response
from flask_bootstrap import Bootstrap
import json
import datetime

app = Flask(__name__, static_url_path='/static')
Bootstrap(app)

values = ['1', '2', '3', '4', '5']
topic1 = {'id': 't1',
          'title': 'Can the Cloud be Secure?! (Renato Kuiper, Tesorion)'}
topic2 = {'id': 't2',
          'title': 'Cyber Threat Intelligence (Michael Jones, ING)'}
topic3 = {'id': 't3',
          'title': 'Hack#ING workshop: with live OWASP labs (Glenn ten Cate, '
                   'ING)'}
topic4 = {'id': 't4',
          'title': 'Overall pizza session: Another Slice of Security'}
topics = [topic1, topic2, topic3, topic4]

filename = 'data.txt'
feedback_list = []


@app.route('/')
def root():
    return render_template('poll.html', topics=topics, values=values)


def getcookie():
    name = request.cookies.get('quest4dave')
    if name:
        return True
    else:
        return False


@app.route('/poll')
def poll():

    feedback = dict(request.args.items())
    print(feedback)
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
    message = 'Thank you for your feedback!'
    return render_template('default_response.html', message=message)


@app.route('/youalreadyvoted')
def alreadyvoted():
    message = 'Computer says: "No, you already voted." :('
    return render_template('default_response.html', message=message)


@app.route('/results')
def show_results():
    votes = {}
    topic1_score = 0
    topic2_score = 0
    topic3_score = 0
    topic4_score = 0
    counter = 0
    remarks = []
    for val in values:
        votes[val] = 0

    try:
        with open(filename, 'r') as read_file:
            feedback_list = json.load(read_file)
        for feedback in feedback_list:
            topic1_score += int(feedback[topic1['id']])
            topic2_score += int(feedback[topic2['id']])
            topic3_score += int(feedback[topic3['id']])
            topic4_score += int(feedback[topic4['id']])
            counter += 1
            remarks.append(feedback['textarea1'])
        scores = [{'topic': topic1['title'], 'score': topic1_score},
                  {'topic': topic2['title'], 'score': topic2_score},
                  {'topic': topic3['title'], 'score': topic3_score},
                  {'topic': topic4['title'], 'score': topic4_score}]
    except json.decoder.JSONDecodeError:
        scores = []
    return render_template('results.html', scores=scores,
                           counter=counter, remarks=remarks)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
