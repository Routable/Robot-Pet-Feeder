from flask import Flask, jsonify, abort, url_for, render_template, make_response, request, redirect, flash
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.secret_key = 'some_secret'

auth = HTTPBasicAuth()


# Code to manage hardware devices, such as camera, motors, and pumps.
import action_handler
action_handler.motor_setup()


    
###################################
# <--------- ROUTES -------------->
###################################

@app.route('/', methods=['GET'])
def home():
  labels = ['Monday', 'Tuesday', 'Wednesday']
  values = [3, 3, 6]
  action_handler.get_video_feed()
  return render_template('index.html', title='Feeding History', max=3, labels=labels, values=values)


@app.route('/feed', methods=['POST'])
def feed():

  small = 3
  medium = 6
  large = 10

  if request.method == "POST":
    feeding_size = request.form.get("size", None)
    if feeding_size is not None:
      flash('Feeding is in progress.')
      if feeding_size == "Small":
        action_handler.enable_motor(small)
      elif feeding_size == "Medium":
        action_handler.enable_motor(medium)
      elif feeding_size == "Large":
        action_handler.enable_motor(large)
      return redirect(url_for('home'))
    return redirect(url_for('home'))


@app.route('/schedule', methods=['POST'])
def schedule():
  if request.method == "POST":
    date = request.form.get("datetime", None)
    action_handler.scheduled(date)
    flash('Scheduled feeding set for ' + str(date))
    return redirect(url_for('home'))


# Emergency Stop For Motors
@app.route('/stop', methods=['POST'])
def stop():
  if request.method == "POST":
    action_handler.disable_motor()
    flash("The feeder has been stopped by the user.")
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')