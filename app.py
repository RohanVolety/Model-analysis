import io
from distutils.log import debug
from fileinput import filename
import pandas as pd
from flask import *
import os
from werkzeug.utils import secure_filename
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask
import numpy as np
import matplotlib.pyplot as plt



UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')

# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)

# Configure upload file path flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = 'This is your secret key to utilize session in Flask'

@app.route('/', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
      # upload file flask
        f = request.files.get('file')

        # Extracting uploaded file name
        data_filename = secure_filename(f.filename)

        f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            data_filename))

        session['uploaded_data_file_path'] =os.path.join(app.config['UPLOAD_FOLDER'],data_filename)

        return render_template('index2.html')
    return render_template("index.html")


@app.route('/show_data')
def showData():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)
    # read csv
    uploaded_df = pd.read_csv(data_file_path, encoding='latin-1', error_bad_lines=False)
    # Converting to html Table
    uploaded_df_html = uploaded_df.to_html()
    return render_template('show_csv_data.html',data_var=uploaded_df_html)




@app.route('/print-plot')
def plot():
    data = pd.read_csv(r"staticFiles\uploads\hello.csv")
    plt.plot(data['model_output'],data['model_target'])
    plt.xlabel('X Axis Label')
    plt.ylabel('Y Axis Label')
    plt.title('Plot Title')
    plt.savefig('static/plot.png')
    return render_template('plot.html', plot='./static/plot.png')



if __name__ == '__main__':
    app.run(debug=True)
