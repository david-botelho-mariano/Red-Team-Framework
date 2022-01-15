#webserver
from flask import Flask, render_template, request
import os

#generic tools
import subprocess

#nmap
from xml.dom import minidom

#screenshotpy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

base_folder = os.getcwd() 
app = Flask(__name__)

def save_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

##http://127.0.0.1:5000/
@app.route("/")
def index():

    return render_template("index.html")

#http://127.0.0.1:5000/reconnaissance/tj.to.gov.br/
@app.route("/reconnaissance/<website_url>/")
def website_url(website_url):

    return render_template("reconnaissance.html")    

#http://127.0.0.1:5000/programs/amass?target=www.google.com
@app.route("/programs/amass")
def amass():

    target = request.args.get("target")
    args = [base_folder + '/tools/amass/amass.exe', 'enum', '-active', '-d', target]
    print(args)

    amass_result = subprocess.check_output(args)
    print(amass_result)

    try:
        os.mkdir(base_folder + "/static/targets/" + target)

    except Exception as error:
        pass

    finally:
        amass_filename = base_folder + "/static/targets/" + target + "/amass.txt"
        print(amass_filename)

        save_file(amass_filename, amass_result)
    
    return str(amass_result)

#http://127.0.0.1:5000/programs/nmap?target=www.google.com
@app.route("/programs/nmap")    
def nmap():
    
    target = request.args.get("target")
    subdomains_path = base_folder + "/static/targets/" + target + "/amass.txt"
    output_path = base_folder + "/static/targets/" + target + "/nmap.xml"
    nmap_filename_clean = base_folder + "/static/targets/" + target + "/nmap_clean.txt"

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

#http://127.0.0.1:5000/programs/screenshots?target=www.google.com
@app.route("/programs/screenshots")    
def screenshotpy():

    webdriver_path = base_folder + "/tools/chrome/chrome-driver.exe"
    print(webdriver_path)

    chrome_path = base_folder + "/tools/chrome/chrome.exe"
    print(chrome_path)

    chrome_opcoes = Options()
    chrome_opcoes.add_argument("--headless")
    chrome_opcoes.add_argument("--log-level=3")
    chrome_opcoes.add_argument("--start-maximized")
    chrome_opcoes.binary_location = chrome_path
    chrome_navegador = webdriver.Chrome(webdriver_path, chrome_options=chrome_opcoes)
    chrome_navegador.set_page_load_timeout(10)

    target = request.args.get("target")

    nmap_result_path = base_folder + "/static/targets/" + target + "/nmap_clean.txt"
    print(nmap_result_path)

    try:
        os.mkdir(base_folder + "/static/targets/" + target + "/prints")

    except Exception as error:
        pass

    screenshots_folder = base_folder + "/static/targets/" + target + "/prints"
    print(screenshots_folder)

    with open(nmap_result_path, 'r') as f:
    	for linha in f.read().splitlines():

            print(linha)
            
            try:

                chrome_navegador.get('https://' + linha)
                chrome_navegador.save_screenshot(screenshots_folder + '/https_'+ linha.replace('.', '_').replace(':', '-') + '.png')

                chrome_navegador.get('http://' + linha)
                chrome_navegador.save_screenshot(screenshots_folder + '/http_'+ linha.replace('.', '_').replace(':', '-') + '.png')
                
            except Exception as erro:
                print("[+]FALHA", erro)

    chrome_navegador.close()
            
    return "success"

#http://127.0.0.1:5000/results
@app.route("/results/")
def results_folders():

    paths = os.listdir(base_folder + "/static/targets")

    html_paths = ""

    for path in paths:
        html_paths += "<a target='_blank' href='/results/" + path + "'>" + path + "</a><br>"
        print(path)

    print(html_paths)
    return render_template('results.html', html_paths=html_paths)

#http://127.0.0.1:5000/results/google.com/
@app.route("/results/<website_url>/")
def results_files(website_url):

    paths = os.listdir(base_folder + "/static/targets/" + website_url)

    html_paths = ""

    for path in paths:

        if "prints" in path:
            html_paths += "<a target='_blank' href='/results/" + website_url + "/prints'>" + path + "</a><br>"

        else:
            html_paths += "<a target='_blank' href='/static/targets/" + website_url + "/" + path + "'>" + path + "</a><br>"

        print(path)

    print(html_paths)
    return render_template('results.html', html_paths=html_paths, website_url=website_url)    

#http://127.0.0.1:5000/results/google.com/prints/
@app.route("/results/<website_url>/prints/")
def results_images(website_url):

    paths = os.listdir(base_folder + "/static/targets/" + website_url + "/prints")
    print(paths)

    html_paths = ""

    for path in paths:

        html_paths += '''   <figure class="figure">
                                <img src="/static/targets/{website_url}/prints/{path}" class="figure-img img-fluid rounded">
                                <figcaption class="figure-caption">{path}</figcaption>
                            </figure>
                      '''.format(website_url=website_url, path=path)
        print(path)

    print(html_paths)
    return render_template('results.html', html_paths=html_paths, website_url=website_url)

if __name__ == '__main__':    
    app.run(debug=True)