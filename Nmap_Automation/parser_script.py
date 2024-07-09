import xml.etree.ElementTree as ET
import csv

def parse_xml_to_csv(xml_file, csv_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Open CSV file for writing
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the CSV header
        header = [
            'IP Address', 'MAC Address', 'Vendor', 'Port', 'Protocol', 'State', 
            'Service Name', 'Service Product', 'Service Version', 'Service Extra Info',
            'OS Match', 'OS Accuracy', 'OS Type', 'OS Vendor', 'OS Family', 'OS Generation',
            'Uptime Seconds', 'Last Boot', 'Host Script ID', 'Host Script Output'
        ]
        writer.writerow(header)
        
        # Iterate over each host
        for host in root.findall('host'):
            # Get IP address
            ip_address = host.find("address[@addrtype='ipv4']").attrib.get('addr', '')

            # Get MAC address and vendor if available
            mac_element = host.find("address[@addrtype='mac']")
            if mac_element is not None:
                mac_address = mac_element.attrib.get('addr', '')
                vendor = mac_element.attrib.get('vendor', '')
            else:
                mac_address = ''
                vendor = ''

            # Get uptime information
            uptime_element = host.find('uptime')
            if uptime_element is not None:
                uptime_seconds = uptime_element.attrib.get('seconds', '')
                last_boot = uptime_element.attrib.get('lastboot', '')
            else:
                uptime_seconds = ''
                last_boot = ''

            # Get OS match information
            os_match_element = host.find('os/osmatch')
            if os_match_element is not None:
                os_match = os_match_element.attrib.get('name', '')
                os_accuracy = os_match_element.attrib.get('accuracy', '')
                os_class_element = os_match_element.find('osclass')
                if os_class_element is not None:
                    os_type = os_class_element.attrib.get('type', '')
                    os_vendor = os_class_element.attrib.get('vendor', '')
                    os_family = os_class_element.attrib.get('osfamily', '')
                    os_generation = os_class_element.attrib.get('osgen', '')
                else:
                    os_type = ''
                    os_vendor = ''
                    os_family = ''
                    os_generation = ''
            else:
                os_match = ''
                os_accuracy = ''
                os_type = ''
                os_vendor = ''
                os_family = ''
                os_generation = ''

            # Get host script information
            host_scripts = host.findall('hostscript/script')
            if host_scripts:
                for script in host_scripts:
                    script_id = script.attrib.get('id', '')
                    script_output = script.attrib.get('output', '')
            else:
                script_id = ''
                script_output = ''

            # Iterate over each port
            ports = host.findall('ports/port')
            if ports:
                for port in ports:
                    port_id = port.attrib.get('portid', '')
                    protocol = port.attrib.get('protocol', '')
                    state = port.find('state').attrib.get('state', '')

                    # Get service information
                    service_element = port.find('service')
                    if service_element is not None:
                        service_name = service_element.attrib.get('name', '')
                        service_product = service_element.attrib.get('product', '')
                        service_version = service_element.attrib.get('version', '')
                        service_extrainfo = service_element.attrib.get('extrainfo', '')
                    else:
                        service_name = ''
                        service_product = ''
                        service_version = ''
                        service_extrainfo = ''

                    # Write row to CSV
                    row = [
                        ip_address, mac_address, vendor, port_id, protocol, state, 
                        service_name, service_product, service_version, service_extrainfo,
                        os_match, os_accuracy, os_type, os_vendor, os_family, os_generation,
                        uptime_seconds, last_boot, script_id, script_output
                    ]
                    writer.writerow(row)
            else:
                # If no ports are listed, write a row with host information only
                row = [
                    ip_address, mac_address, vendor, '', '', '', 
                    '', '', '', '',
                    os_match, os_accuracy, os_type, os_vendor, os_family, os_generation,
                    uptime_seconds, last_boot, script_id, script_output
                ]
                writer.writerow(row)

if __name__ == "__main__":
    parse_xml_to_csv('output.xml', 'output.csv')
