from flask import Flask, render_template, send_file
import common
import datetime

app = Flask(__name__)

@app.route('/positive.png')
def pos():
	return send_file('positive.png', mimetype='image/png')

@app.route('/negative.png')
def neg():
	return send_file('negative.png', mimetype='image/png')

@app.route('/1')
def team1():
	return render_template("./page.html",
        team = 1,
        checks = common.getChecksPerTeam(1))

'''
@app.route('/2')
def team1():
	return render_template("./page.html",
        team = 1,
        checks = common.getChecksPerTeam(2))

@app.route('/3')
def team1():
	return render_template("./page.html",
        team = 1,
        checks = common.getChecksPerTeam(3))

@app.route('/4')
def team1():
	return render_template("./page.html",
        team = 1,
        checks = common.getChecksPerTeam(4))

@app.route('/5')
def team1():
	return render_template("./page.html",
        team = 1,
        checks = common.getChecksPerTeam(5))
'''

app.run(debug = True, host='0.0.0.0')
