#!/usr/bin/env python3
#Python script for returning the geolocation and ownership of an IP Address
import requests
import optparse
from bs4 import BeautifulSoup
from tabulate import tabulate
import csv

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




#get arguments from input
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--ip_addr", dest="ip_addr", help="IP Address to search for")
    parser.add_option("-f", "--fields", dest="fields", help="fields to search for, enter a comma seperated list or skip option for default: field,field1,field2")
    parser.add_option("-c", "--csv", dest="csv", action="store_true", help="output to a csv file")
    parser.add_option("--lf", "--list_fields", dest="list_fields", action="store_true", help="list all the possible fields")
    parser.add_option("-a", "--api_key", dest="api_key", help="Enter your API key")
    (options, arguments) = parser.parse_args()
    if not options.api_key:
        parser.error("[-] Please enter your API key from https://ipgeolocation.io/")
    if not options.ip_addr:
        if not options.list_fields:
        	parser.error("[-] Please specify an IP address, use --help for more info")
    if not options.fields:
    	options.fields = "continent_code,country_name,country_code2,state_prov,city,isp,organization"
    return options


#connect to the url and return the dict output
def connect_url(ip_addr, fields, api_key):
	url= f"https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip_addr}&fields={fields}&include=liveHostname"
	r = requests.get(url)
	output = r.json()
	return output


#create the table using tabulate
def create_output(data):
	print(tabulate(data.items()))


#output to csv
def output_csv(data):
	with open("ip_address_output.csv", "w+", encoding='UTF8') as f:
		writer = csv.writer(f)
		writer.writerow(data.keys())
		writer.writerow(data.values())
		f.close()



options = get_arguments()
if options.list_fields:
	for line in field_list:
		print(line)
	exit()
output = connect_url(options.ip_addr, options.fields, options.api_key)
create_output(output)
if options.csv:
	output_csv(output)
