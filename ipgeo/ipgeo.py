#!/usr/bin/python3
import requests
import optparse
import csv
from colorama import Fore
import ipaddress
from pwn import *

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
    "geoname_id",
    
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



		

#Function to get arguments from input
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--ip_addr", dest="ip_addr", help="IP Address to search for")
    parser.add_option("-f", "--fields", dest="fields", help="fields to search for, enter a comma seperated list: field,field1,field2")
    parser.add_option("--lf", "--list_fields", dest="list_fields", action="store_true", help="list all the possible fields")
    parser.add_option("-a", "--api_key", dest="api_key", help="Enter your API key")
    parser.add_option("-k", "--api_key_file", dest="api_key_file", help="Enter the filename where the API key is stored, must contain only one line with the API key")
    parser.add_option("-F", "--file_list", dest="file_list", help="Enter your API key")
    parser.add_option("-n", "--cidr_notation", dest="cidr_notation", help="Enter an IP Address range using CIDR ex: 192.168.1.0/24")
    parser.add_option("-o", "--output_file", dest="output_file", help="File name for the csv output, default is whodis_lookup.csv")
    parser.add_option("-H", "--hide_output", dest="hide_output", action="store_true", help="Hide the output")
    (options, arguments) = parser.parse_args()
    if not options.ip_addr:
    	if not options.file_list:
    		if not options.cidr_notation:
        		if not options.list_fields:
        			parser.error("[-] Please either specify an IP address, file list of IPs, CIDR or -lf to list fields, use --help for more info")
    if not options.fields:
    	options.fields = "continent_name,country_name,country_code2,state_prov,city,organization,latitude,longitude"
    if not options.api_key and not options.list_fields and not options.api_key_file:
    	parser.error("[-] Please enter your API key from https://ipgeolocation.io/")
    return options


#Function to connect to the url and return the dict output
def connect_url(ip_addr, fields, api_key):
	url= f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip_addr}&fields={fields}&include=liveHostname"
	r = requests.get(url)
	output = r.json()
	return output


#Function to create the output in the terminal
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


#Function to output to csv
def output_csv(data):
	with open(options.output_file, "a", encoding='UTF8') as f:
		writer = csv.writer(f)
		writer.writerow(data.values())
		f.close()


#Function to create headers for CSV file based on options.fields
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


#Function for main program
#Determines if single ip, CIDR or a list of ips are given
#Then loops through each ip using the ipgeo API via connect_url function
#All IP addresses are added to ip_list = []


def main_program():

	with log.progress("Searching Geolocation and Owner information") as p:
		if options.output_file:
			create_headers()
		ip_list = []

		if options.file_list:
			orig_list = open(options.file_list, "r")
			for line in orig_list:
				ip_list.append(line)

		elif options.cidr_notation:
			for ip in ipaddress.IPv4Network(options.cidr_notation):
				ip_list.append(ip)

		elif options.ip_addr:
			ip_list.append(options.ip_addr)

		for ip in ip_list:
			output = connect_url(ip, options.fields, options.api_key)
			p.status("IP: {}".format(ip))
			if options.output_file:
				output_csv(output)
			if not options.hide_output:
				create_output(output)



#function calls
try:
	options = get_arguments()
	if options.api_key_file:
		with open(options.api_key_file, "r") as f:
			options.api_key = f.readline()
	if options.list_fields:
			for line in field_list:
				print(line)
			print("\nEnter these fields in the format field1,field2,field3,field4\n")
			exit()
	main_program()
except KeyboardInterrupt:
	print("\n[-] Ctrl + C detected, exiting now.")