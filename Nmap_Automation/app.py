import subprocess
import xml.etree.ElementTree as ET
import csv
from flask import Flask, render_template, request

from n_parser import parse_nmap_xml_to_csv  # Import the function from n_parser.py
from parser_script import parse_xml_to_csv  # Import the function from parser_script.py

app = Flask(__name__)

def is_compatible(flags):
    incompatible_sets = [
        {'-sL', '-sn'},  # List scan and skip port scan are incompatible with other scan types
        {'-sA', '-sT'},  # TCP ACK scan can't be used with TCP connect scan
        {'-sP', '-sL'},  # ARP scan can't be used with list scan
        {'-O', '-f'},    # OS detection is incompatible with fragmented packets
    ]

    for incomp_set in incompatible_sets:
        if len(incomp_set.intersection(flags)) > 1:
            return False, incomp_set.intersection(flags)
    return True, None

def run_nmap(ip_range, mode, scan_types=None, host_discovery_types=None, port_selection=None, custom_ports=None, service_detection_types=None, firewall_options=None, output_format=None, nmap_scripts=None):
    selected_flags = []

    if mode == '2':  # Advanced mode
        if host_discovery_types:
            for hdt in host_discovery_types:
                selected_flags.append(hdt)

        if '-sn' in selected_flags:
            scan_types = []
            service_detection_types = []
            port_selection = ""

        if scan_types:
            for st in scan_types:
                selected_flags.append(st)

        if port_selection == 'custom' and custom_ports:
            selected_flags.append(f"-p {custom_ports}")
        elif port_selection == 'default':
            selected_flags.append("-p 1-1024")

        if service_detection_types:
            for sdt in service_detection_types:
                selected_flags.append(sdt)

        if firewall_options:
            for fo in firewall_options:
                selected_flags.append(fo)

        if nmap_scripts:
            for script in nmap_scripts:
                selected_flags.append(script)

        if output_format:
            selected_flags.append(output_format)

    compatible, incomp_flags = is_compatible(set(selected_flags))
    if not compatible:
        raise ValueError(f"Selected flags are not compatible with each other: {', '.join(incomp_flags)}")

    nmap_command = f"sudo nmap {ip_range} {' '.join(selected_flags)} -oX output.xml"
    
    # Run nmap command and wait for it to complete
    result = subprocess.run(nmap_command, shell=True, capture_output=True, text=True)
    print(result.stdout)  # Debugging: print nmap output
    print(result.stderr)  # Debugging: print nmap errors if any

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        ip_range = request.form['ip_range']
        mode = request.form['mode']
        scan_types = request.form.getlist('scan_types')
        host_discovery_types = request.form.getlist('host_discovery_types')
        port_selection = request.form['port_selection']
        custom_ports = request.form['custom_ports'] if port_selection == 'custom' else None
        service_detection_types = request.form.getlist('service_detection_types')
        firewall_options = request.form.getlist('firewall_options')
        output_format = request.form['output_format']
        nmap_scripts = request.form.getlist('nmap_scripts')

        try:
            if mode == '1':
                # Run nmap with basic settings
                run_nmap(ip_range, mode)
                # Parse XML to CSV for n_result.html
                parse_xml_to_csv('output.xml', 'output.csv')
                
                # Read output.csv and pass to template for rendering
                results = []
                with open('output.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    headers = next(reader)  # skip header
                    for row in reader:
                        results.append(row)

                return render_template('n_result.html', headers=headers, results=results)
            else:
                # Run nmap with advanced settings
                run_nmap(ip_range, mode, scan_types, host_discovery_types, port_selection, custom_ports, service_detection_types, firewall_options, output_format, nmap_scripts)
                
                # Parse XML to CSV for results.html
                parse_xml_to_csv('output.xml', 'output.csv')

                # Read output.csv and pass to template for rendering
                results = []
                with open('output.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    headers = next(reader)  # skip header
                    for row in reader:
                        results.append(row)

                return render_template('results.html', headers=headers, results=results)
        except ValueError as e:
            return render_template('index.html', error=str(e))
    else:
        return render_template('results.html')

@app.route('/script_results', methods=['GET', 'POST'])
def script_results():
    if request.method == 'GET':

        try:
            # Parse XML to CSV using n_parser.py function for script_results.html
            parse_nmap_xml_to_csv('output.xml', 'o1.csv')
            
            # Read o1.csv and pass to template for rendering
            results = []
            with open('o1.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  # skip header
                for row in reader:
                    results.append(row)

            return render_template('script_results.html', headers=headers, results=results)
        except ValueError as e:
            return render_template('index.html', error=str(e))
    else:
        return render_template('script_results.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
