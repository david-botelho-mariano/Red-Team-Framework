from flask import Flask, render_template
import subprocess

import os
#os.path.join(os.path.dirname(__file__), 'static')

base_folder = os.getcwd() 
app = Flask(__name__)

def save_file(file):
    with open(base_folder + "/" + file.filename, 'wb') as f:
        f.write(file.read())

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/config")
def config():

    return render_template("config.html")    

@app.route("/programs/amass")    
def amass():

    args = [base_folder + '/tools/amass.exe', 'enum', '-active', '-d', 'tce.to.gov.br']
    print(args)

    amass_result = subprocess.check_output(args)
    print(amass_result)
    return str(amass_result)

if __name__ == '__main__':    
	app.run(debug=True)      


