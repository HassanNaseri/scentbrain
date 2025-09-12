from flask import Flask, render_template
import os

application = app = Flask(__name__)
app.config['IMAGE_FOLDER'] = os.path.join('static', 'images')

@app.route('/')
@app.route('/index')
def show_index():
    full_filename = os.path.join(app.config['IMAGE_FOLDER'], 'scentbrain-logo.png')
    return render_template("index.html", logo = full_filename)
