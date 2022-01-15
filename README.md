# Red Team Framework

This is a Grapical user interface (GUI) to automate the use of penetration test tools, for example: in reconnaissance mode, with a click you can enumerate domains using Amass, then it will check which hosts are alive and what are the ports open using Nmap, then it will take screenshots of the live websites.


# Tools implemented

  - [X] Amass (https://github.com/OWASP/Amass)
  - [X] Nmap (https://nmap.org)
  - [X] Screenshot websites


# Demonstration

<table>
  <tr>
    <td valign="top"><img src="https://user-images.githubusercontent.com/48680041/149572643-00bb9955-fe4f-4a27-a809-2971c5b22d98.png"></td>
    <td valign="top"><img src="https://user-images.githubusercontent.com/48680041/149610607-27d55201-204a-4a3f-9050-87f05354f19c.png"></td>
  </tr>
 </table>

![image](https://user-images.githubusercontent.com/48680041/149572643-00bb9955-fe4f-4a27-a809-2971c5b22d98.png)

![image](https://user-images.githubusercontent.com/48680041/149610607-27d55201-204a-4a3f-9050-87f05354f19c.png)


# Getting started 

1) Install python libraries:
- `pip install flask` 
- `pip install selenium`

2) Start the framework
- `python app.py`


# TO-DO

  - [ ] Shodan (https://www.shodan.io)
  - [ ] Chaos (https://chaos.projectdiscovery.io)
  - [ ] Gau (https://github.com/lc/gau)
  - [ ] Metasploit (https://docs.rapid7.com/metasploit/pro-feature-api)
  - [ ] Burp Suite (https://portswigger.net/blog/burps-new-rest-api)
  - [ ] Nettacker (https://github.com/OWASP/Nettacker)
  - [ ] Brutespray (https://github.com/x90skysn3k/brutespray)
  - [ ] Acunetix (https://www.acunetix.com/blog/docs/managing-scans-python-acunetix-api)
  - [ ] Joomscan (https://github.com/OWASP/joomscan)
  - [ ] Wpscan (https://github.com/wpscanteam/wpscan)
  - [ ] Find endpoints using JS files

- [ ] Add elegant template
  - https://adminlte.io/
  - https://startbootstrap.com/theme/sb-admin-2
  - https://coreui.io/?affChecked=1#compare
