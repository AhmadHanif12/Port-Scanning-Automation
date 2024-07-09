import xml.etree.ElementTree as ET
import csv

def parse_nmap_xml_to_csv(xml_file, csv_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Open CSV file for writing
    with open(csv_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write the header row
        header = ["IP Address", "Hostname", "Port", "State", "Service", "Version", "Script ID", "Script Output"]
        csvwriter.writerow(header)

        for host in root.findall('host'):
            ip_addr = host.find('address').get('addr')
            hostname = host.find('hostnames/hostname').get('name') if host.find('hostnames/hostname') is not None else 'N/A'

            for port in host.findall('ports/port'):
                port_id = port.get('portid')
                state = port.find('state').get('state')
                service = port.find('service').get('name')
                version = port.find('service').get('version', '')

                # Check for script outputs
                for script in port.findall('script'):
                    script_id = script.get('id')
                    script_output = script.get('output')
                    csvwriter.writerow([ip_addr, hostname, port_id, state, service, version, script_id, script_output])

                # If no script output, write the basic details
                if not port.findall('script'):
                    csvwriter.writerow([ip_addr, hostname, port_id, state, service, version, '', ''])

if __name__ == "__main__":
    xml_file = 'output.xml'
    csv_file = 'o1.csv'
    parse_nmap_xml_to_csv(xml_file, csv_file)
