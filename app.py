from flask import Flask, render_template, request
import subprocess
import os
from xml.dom import minidom

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
        os.mkdir(base_folder + "/targets/" + target)

    except Exception as error:
        pass

    finally:
        amass_filename = base_folder + "/targets/" + target + "/amass.txt"
        print(amass_filename)

        save_file(amass_filename, amass_result)
    
    return str(amass_result)

@app.route("/programs/nmap")    
def nmap():

    try:
        os.mkdir(base_folder + "/targets/" + target)

    except Exception as error:
        pass

    target = request.args.get("target")
    subdomains_path = base_folder + "/targets/" + target + "/amass.txt"
    output_path = base_folder + "/targets/" + target + "/nmap.xml"
    nmap_filename_clean = base_folder + "/targets/" + target + "/nmap_clean.txt"

    args = [base_folder + '/tools/nmap/nmap.exe', '-T5', '-F', '-Pn', '-iL', subdomains_path, '-oX', output_path]
    print(args)

    nmap_result = subprocess.check_output(args)
    print(nmap_result)

    nmap_result_clean = ""

    xmldoc = minidom.parse(output_path)
    hosts = xmldoc.getElementsByTagName("host")

    for host in hosts:
        hostnames = host.getElementsByTagName("hostnames")
        
        for hostname in hostnames:
            hostname = hostname.getElementsByTagName("hostname")
            hostname = hostname[0].attributes["name"].value
            #print(hostname)

            ports = host.getElementsByTagName("ports")

            for port in ports:
                port = host.getElementsByTagName("port")

                for port in port:
                    port = port.attributes["portid"]
                    port = port.value
                    nmap_result_clean += hostname + ":" + port + "\n"

    save_file(nmap_filename_clean, nmap_result_clean)

    return str(nmap_result)

if __name__ == '__main__':    
	app.run(debug=True)      


