
# PORT Scan-Automation 

## Introduction:
Our project is an advanced web-based automation tool for Nmap, the popular network scanning utility. Designed with a user-friendly interface, this tool allows users to configure and execute Nmap scans effortlessly, even if they have limited technical expertise.

## Key Features:
### IP Range Scanning: 
Easily input single IP addresses or entire ranges for scanning.
### Mode Selection: 
Choose between Normal and Advanced scanning modes.
### Advanced Options:
- #### Scan Types: 
Select from various scan types such as TCP SYN, UDP, and more.
- #### Host Discovery: 
Customize host discovery methods.
- #### Port Selection: 
Default or custom port ranges.
- #### Service Detection: 
Determine service versions and operating systems.
- #### Firewall Evasion: 
Options for evading firewalls and intrusion detection systems.
- #### Nmap Scripting: 
Include specific Nmap scripts for enhanced functionality.
- #### Output Formats: 
Multiple output formats including XML, normal text, and grepable.

## Workflow:
### Input Configuration: 
Users fill out a form specifying the IP range, scan type, and other options.
### Run Nmap: 
The configured Nmap command is executed on the backend.
### Results Parsing: 
XML output from Nmap is parsed into CSV format for easy analysis.
### Results Display: 
Parsed results are displayed on the web interface for user review.

## Getting Started
Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
- *Python 3.6+*

- *pip (Python package installer)*

### Installation

#### Step 1:
Clone the Repository

```bash
https://github.com/AhmadHanif12/Port-Scanning-Automation.git
cd Port-Scanning-Automation
```
#### Step 2:

```bash
cd Nmap_Automation
```
#### Step 3:
Run the App
```bash
sudo python app.py
```

#### Step 4:
Visit http://127.0.0.1:8080/ in your browser

## Contributors:
We are grateful to our wonderful contributors who have helped make this project better. Here are some of the amazing people who have contributed:

### GitHub Profiles:
https://github.com/arslanjv

https://github.com/sirzaighamabq

## Contributing:
#### 🎉 We Welcome Your Contributions! 🎉
Whether you're looking to enhance the functionality, improve the documentation, or add exciting new features, we encourage you to contribute to our project. Your input can help us make this application even better.

## License:
This project is licensed under the MIT License - see the LICENSE.md file for details.




