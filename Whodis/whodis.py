#!/usr/bin/env python3
import requests
import optparse
from bs4 import BeautifulSoup
from tabulate import tabulate
import csv
from colorama import Fore
import ipaddress
import re
import pyfiglet

field_list = [
	"continent_name",
    "country_code2",
    "country_code3",
    "country_name",
    "country_capital",
    "state_prov",
    "district",
    "city",
    "zipcode",
    "latitude",
    "longitude",
    "is_eu",
    "calling_code",
    "country_tld",
    "languages",
    "country_flag",
    "isp",
    "connection_type",
    "organization",
    "geoname_id"
]

field_dic = {
	"ip":"IP Address",
	"continent_name":"Continent",
    "country_code2":"Country Code 2",
    "country_code3":"Country Code 3",
    "country_name":"Country Name",
    "country_capital":"Country Capital",
    "state_prov":"State",
    "district":"District",
    "city":"City",
    "zipcode":"Zipcode",
    "latitude":"Latitude",
    "longitude":"Longitude",
    "is_eu":"Is EU",
    "calling_code":"Calling Code",
    "country_tld":"Country TLD",
    "languages":"Languages",
    "country_flag":"Country Flag",
    "isp":"ISP",
    "connection_type":"Connection Type",
    "organization":"Organization",
    "geoname_id":"Geoname ID"

}



		

#get arguments from input
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--ip_addr", dest="ip_addr", help="IP Address to search for")
    parser.add_option("-f", "--fields", dest="fields", help="fields to search for, enter a comma seperated list: field,field1,field2")
    parser.add_option("-c", "--csv", dest="csv", action="store_true", help="output to a csv file")
    parser.add_option("--lf", "--list_fields", dest="list_fields", action="store_true", help="list all the possible fields")
    parser.add_option("-a", "--api_key", dest="api_key", help="Enter your API key")
    parser.add_option("-F", "--file_list", dest="file_list", help="Enter your API key")
    parser.add_option("-n", "--cidr_notation", dest="cidr_notation", help="Enter an IP Address range using CIDR ex: 192.168.1.0/24")
    parser.add_option("-o", "--output_file", dest="output_file", help="File name for the csv output, default is whodis_lookup.csv")
    (options, arguments) = parser.parse_args()
    if not options.api_key:
    	parser.error("[-] Please enter your API key from https://ipgeolocation.io/")
    if not options.ip_addr:
    	if not options.file_list:
    		if not options.cidr_notation:
        		if not options.list_fields:
        			parser.error("[-] Please either specify an IP address, file list of IPs, CIDR or -lf to list fields, use --help for more info")
    if not options.fields:
    	options.fields = "continent_name,country_name,country_code2,state_prov,city,isp,organization"
    return options


#connect to the url and return the dict output
def connect_url(ip_addr, fields, api_key):
	url= f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip_addr}&fields={fields}&include=liveHostname"
	r = requests.get(url)
	output = r.json()
	return output


#create the table using tabulate
def create_output(data):
	#print(tabulate(data.items(), tablefmt="fancy_grid"))
	print(Fore.GREEN + f"[+] Output for {data['ip']}")
	del data['ip']
	for entry in data:
		first_col_length = 20
		new_word = field_dic[entry]
		diff = first_col_length - len(new_word)
		new_entry = (new_word + (" " * diff))
		print(Fore.RED + new_entry + "	" + Fore.RESET + data[entry])
	print("\n\n")

#output to csv
def output_csv(data):
	with open(options.output_file, "a", encoding='UTF8') as f:
		writer = csv.writer(f)
		writer.writerow(data.values())
		f.close()

#create headers for CSV file based on options.fields
def create_headers():
	new_headers = []
	new_headers.append("IP Address")
	create_headers = (options.fields).split(",")
	for entry in create_headers:
		new_headers.append(field_dic[entry]) 
	with open(options.output_file, "w+", encoding='UTF8') as f:
		writer = csv.writer(f)
		writer.writerow(new_headers)
	f.close()





#function for a single ip_addr -i
def single_program():		
	output = connect_url(options.ip_addr, options.fields, options.api_key)
	create_output(output)
	if options.csv:
		create_headers()
		output_csv(output)


#function to handle a file list -F
def mul_program():
	
	if options.csv:
		create_headers()
	ip_list = open(options.file_list, "r")
	for line in ip_list:
		options.ip_addr = line
		output = connect_url(options.ip_addr, options.fields, options.api_key)
		if options.csv:
			output_csv(output)
		create_output(output)
	
#function to handle CIDR
def cidr_notation():
	if options.csv:
		create_headers()
	cidr_list = []
	for ip in ipaddress.IPv4Network(options.cidr_notation):
		cidr_list.append(ip)
	for ip in cidr_list:
		options.ip_addr = ip
		output = connect_url(options.ip_addr, options.fields, options.api_key)
		if options.csv:
			output_csv(output)
		create_output(output)


#function calls
try:
	options = get_arguments()
	if options.output_file:
		csv_filename = options.output_file
	else:
		options.output_file = "whodis_output.csv"
	if options.list_fields:
			for line in field_list:
				print(line)
			exit()
	if options.ip_addr:
		single_program()	
	elif options.file_list:
		mul_program()
	elif options.cidr_notation:
		cidr_notation()
except KeyboardInterrupt:
	print("\n[-] Ctrl + C detected, exiting now.")