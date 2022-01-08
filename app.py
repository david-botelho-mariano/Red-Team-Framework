from flask import Flask, render_template, request
import subprocess
import os

base_folder = os.getcwd() 
app = Flask(__name__)

def save_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/reconnaissance/<website_url>/")
def website_url(website_url):

    return render_template("reconnaissance.html")    

@app.route("/programs/amass")    
def amass():

    target = request.args.get("target")
    args = [base_folder + '/tools/amass/amass.exe', 'enum', '-active', '-d', target]
    print(args)

    amass_result = subprocess.check_output(args)
    print(amass_result)

    try:
        os.mkdir(base_folder + "/" + target)

    except Exception as error:
        pass

    finally:
        amass_filename = base_folder + "/" + target + "/amass.txt"
        print(amass_filename)

        save_file(amass_filename, amass_result)
    
    return str(amass_result)

if __name__ == '__main__':    
	app.run(debug=True)      


