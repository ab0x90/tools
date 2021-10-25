#!/usr/bin/python3
import requests
import optparse
import socket
from colorama import Fore
from pwn import *


#Function to get arguments from the command line
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file_list", dest="file_list", help="File with a list of URLs")
    parser.add_option("-u", "--url", dest="url", help="Enter a single URL")
    (options, arguments) = parser.parse_args()
    return options



#Function to open a file and return the list of URLs
def open_file(file_list):
	with open(options.file_list, "r") as f:
		for line in f.readlines():
			line = line.strip()
			url_list.append(line)
	f.close()
	return url_list		





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
		print(f"Server: {url_connect.headers['Server']}")
	if 'https' in url:
		if "Strict-Transport-Security" not in url_connect.headers:
			print(Fore.RED + f"{url}" + Fore.RESET + " is missing the Strict-Transport-Security Header")
	if "Content-Security-Policy" not in url_connect.headers:
		print(Fore.RED + f"{url}" + Fore.RESET + " is missing the Content-Security-Policy Header")
	if "X-Frame-Options" not in url_connect.headers:
		print(Fore.RED + f"{url}" + Fore.RESET + " is missing the X-Frame-Options Header")




#Function calls
options = get_arguments()
url_list = []
if options.url:
	print(options.url)
	url_list.append(options.url)
if options.file_list:
	url_list = open_file(options.file_list)
for url in url_list:
	try:
		check_headers(url)
		with log.progress(f"Checking headers on {url}") as p:
			print('\n\n\n')
	except requests.exceptions.RequestException as e:
		print("[" + Fore.RED + "-" + Fore.RESET + "]" + f"There was a connection error on {url}")
		print('\n\n\n')













