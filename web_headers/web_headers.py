#!/usr/bin/python3
import requests
import optparse
import socket
from colorama import Fore
from pwn import *


#Create lists for storing urls/ips
csp_list = []
hsts_list = []
xframe_list = []
contenttype_list = []
xss_list = []


#Function to get arguments from the command line
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file_list", dest="file_list", help="File with a list of URLs")
    parser.add_option("-u", "--url", dest="url", help="Enter a single URL")
    parser.add_option("-o", "--output", dest="output", action="store_true", help="Enter the name of the Folder for the output to be stored. Files are created for each missing Header and IPs are added to each respective file.")
    (options, arguments) = parser.parse_args()
    if not options.file_list and not options.url:
    	print("[" + Fore.RED + "-" + Fore.RESET + "]" + f" You must enter either a URL(-u) or a file or URLS(-f), type -h for more info")
    return options



#Function to open a file and return the list of URLs
def open_file(file_list):
	with open(options.file_list, "r") as f:
		for line in f.readlines():
			line = line.strip()
			url_list.append(line)
	f.close()
	return url_list		

#Function to create the output, creates one txt file per missing header, one URL/IP per line in each file
def output():
	if csp_list:
		with open("content-security-policy-missing.txt", "w+") as f:
			for item in range (0, len(csp_list)):
				f.write(csp_list[item] + "\n")
			f.close()
	if hsts_list:
		with open("strict-transport-security-missing.txt", "w+") as f:
			for item in range (0, len(hsts_list)):
				f.write(hsts_list[item] + "\n")
			f.close()
	if xframe_list:
		with open("x-frame-missing.txt", "w+") as f:
			for item in range (0, len(xframe_list)):
				f.write(xframe_list[item] + "\n")
			f.close()	
	if contenttype_list:
		with open("x-content-type-missing.txt", "w+") as f:
			for item in range (0, len(contenttype_list)):
				f.write(contenttype_list[item] + "\n")
			f.close()
	if xss_list:
		with open("x-xss-protection-missing.txt", "w+") as f:
			for item in range (0, len(xss_list)):
				f.write(xss_list[item] + "\n")
			f.close()
			
				





#Main function of the tool
def check_headers(url):
	#Connect to the url, split url to 'www.domain.com' and get the IP address using socket.gethostbyname. 
	url_connect = requests.get(url)
	host_url = url.split("/")[2]
	ip_addr = socket.gethostbyname(host_url)


	#Print a banner 
	print("*" * 75)
	print(Fore.GREEN + f"Report for {url} - {ip_addr}" + Fore.RESET)
	print("*" * 75)


	
	#Check for specific headers
	if "Server" in url_connect.headers:
		print(Fore.RED + "Server:" + Fore.RESET + f" {url_connect.headers['Server']}")
	if 'https' in url:
		if "Strict-Transport-Security" not in url_connect.headers:
			print(Fore.RED + "Strict-Transport-Security" + Fore.RESET + " header is missing")
			if options.output:
				hsts_list.append(url + " - " + ip_addr)
	if "Content-Security-Policy" not in url_connect.headers:
		print(Fore.RED + "Content-Security-Policy" + Fore.RESET + " header is missing")
		if options.output:
				csp_list.append(url + " - " + ip_addr)
	if "X-Frame-Options" not in url_connect.headers:
		print(Fore.RED + "X-Frame-Options" + Fore.RESET + " header is missing")
		if options.output:
				xframe_list.append(url + " - " + ip_addr)
	if "X-Content-Type-Options" not in url_connect.headers:
		print(Fore.RED + "X-Content-Type-Options" + Fore.RESET + " header is missing")
		if options.output:
				contenttype_list.append(url + " - " + ip_addr)
	if "X-Xss-Protection" not in url_connect.headers:
			print(Fore.RED + "X-Xss-Protection" + Fore.RESET + " header is missing")
			if options.output:
				xss_list.append(url + " - " + ip_addr)




#Function calls
options = get_arguments()
url_list = []

#determines if the input if a url or url_list
if options.url:
	url_list.append(options.url)
if options.file_list:
	url_list = open_file(options.file_list)

#checks the headers for each url in url_list
for url in url_list:
	#try/except to handle connection errors
	try:
		check_headers(url)
		with log.progress(f"Checking headers on {url}") as p:
			print('\n\n\n')
	except requests.exceptions.RequestException as e:
		print("[" + Fore.RED + "-" + Fore.RESET + "]" + f"There was a connection error on {url}")
		print('\n\n\n')
#if options.output, create the output
if options.output:
	output()










