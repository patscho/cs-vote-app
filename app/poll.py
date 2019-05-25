from flask import Flask, render_template, request, redirect, make_response, send_file
from flask_bootstrap import Bootstrap
import json
import datetime
import yaml


config_file = 'topics.yaml'
results_file = 'results/results.json'
feedback_list = []
app = Flask(__name__, static_url_path='/static')
Bootstrap(app)


def load_config(filename):
    topics = []
    config = yaml.load(open(filename), Loader=yaml.FullLoader)
    for item in config['session_config']:
        if item['type'] == 'talk':
            title = (item['title'] + ' (' + item['speaker'] + ', '
                     + item['company'] + ')')
            topic = {'id': item['id'], 'title': title}
            topics.append(topic)
        elif item['type'] == 'session':
            topic = {'id': item['id'], 'title': item['title']}
            topics.append(topic)
    return topics


def getcookie():
    name = request.cookies.get('quest4dave')
    if name:
        return True
    else:
        return False


@app.route('/')
def root():
    values = ['1', '2', '3', '4', '5']
    return render_template('poll.html', topics=topics, values=values)


@app.route('/poll')
def poll():

    feedback = dict(request.args.items())
    print(feedback)
    if not getcookie():
        feedback_list.append(feedback)
        with open(results_file, mode='w') as my_file:
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
    score = {}
    for t in topics:
        score[t['id']] = 0
    counter = 0
    remarks = []
    scores = []
    try:
        with open(results_file, 'r') as read_file:
            feedback_list = json.load(read_file)
        for feedback in feedback_list:
            for t in topics:
                score[t['id']] += int(feedback[t['id']])
            if feedback['textarea1'] == '':
                remarks.append('-')
            else:
                remarks.append(feedback['textarea1'])
            counter += 1
        for t in topics:
            scores.append({'topic': t['title'], 'score': score[t['id']]})
    except json.decoder.JSONDecodeError:
        scores = []
    return render_template('results.html', scores=scores,
                           counter=counter, remarks=remarks)


@app.route("/results/downloadjson")
def download_json():
    return send_file(results_file, as_attachment=True)


if __name__ == "__main__":
    topics = load_config(config_file)
    app.run(debug=True, host='0.0.0.0')
