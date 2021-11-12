#!/usr/bin/python3

import subprocess
import argparse
import os
import re
import time
from colorama import Fore

#Define Variables
system_list = []
web_check = ["http", "https", "HTTP", "HTTPS"]
green = Fore.GREEN
red = Fore.RED
reset = Fore.RESET



class enum:
	def __init__(self, ipaddr=None, port=None, host=None):
		self.ipaddr = ipaddr
		self.port = port
		self.host = host

	def run_nmap(self):
		os.mkdir(self.ipaddr)
		start_ctime = time.ctime()
		start_time = time.time()
		print(red + f"\n********** Beginning enumeration on {self.ipaddr} **********\n" + reset)
		print(green + "[+]" + reset + f" Beginning nmap scan at {start_ctime}")
		nmap_output =  subprocess.call(["nmap", "-sV", "-sC", "-vv", "-p", "80,443", "-oA", self.ipaddr + "/" + self.ipaddr, self.ipaddr], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		#print(nmap_output)
		end_ctime = time.ctime()
		total_time = (time.time() - start_time)
		print(green + "[+]" + reset + f" Nmap scan ended at {end_ctime}. Scan took {total_time}\n\n")


	def run_ferox_http(self):
		start_ctime = time.ctime()
		start_time = time.time()
		print(green + "[+]" + reset + f" Beginning feroxbuster scan at {start_ctime}")
		ferox_output =  subprocess.call(["feroxbuster", "-u", self.host, "-o", self.ipaddr + "/" + self.ipaddr + "_ferox" + "_" + self.port, "--no-recursion"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		#print(ferox_output)
		end_ctime = time.ctime()
		total_time = (time.time() - start_time)
		print(green + "[+]" + reset + f" Feroxbuster scan ended at {end_ctime}. Scan took {total_time}\n\n")



	def run_ferox_https(self):
		start_ctime = time.ctime()
		start_time = time.time()
		print(green + "[+]" + reset + f" Beginning feroxbuster scan at {start_ctime}")
		ferox_output =  subprocess.call(["feroxbuster", "-u", self.host, "-o", self.ipaddr + "/" + self.ipaddr + "_ferox" + "_" + self.port, "--no-recursion", "-k"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		#print(ferox_output)
		end_ctime = time.ctime()
		total_time = (time.time() - start_time)
		print(green + "[+]" + reset + f" Feroxbuster scan ended at {end_ctime}. Scan took {total_time}\n\n")



	def run_nikto(self):
		start_ctime = time.ctime()
		start_time = time.time()
		print(green + "[+]" + reset + f" Beginning nikto scan at {start_ctime}")
		nikto_output =  subprocess.run(["nikto", "-h", self.host, "-output",  self.ipaddr + "/" + self.ipaddr + "_nikto_"  + self.port + ".txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, input=b"n\r\n")
		#print(nikto_output)
		print("n\r\n")
		end_ctime = time.ctime()
		total_time = (time.time() - start_time)
		print(green + "[+]" + reset + f" Nikto scan ended at {end_ctime}. Scan took {total_time}\n\n")




def get_arguments():
	parser = argparse.ArgumentParser(description='Multi-System Enumeration Tool')
	parser.add_argument('-f', dest='file_list', type=str, help='Text file containing list of IPs to enumerate')
	parser.add_argument('-w', dest='web_enum', action='store_true', help='Perform web enumeration using feroxbuster, if HTTP or HTTPS is found')
	args = parser.parse_args()
	return args


def handle_file(filename):
	with open(filename) as f:
		for line in f:
			system_list.append(line.strip())
		return system_list
		f.close()


def determine_if_http(ipaddr):
	search_list = []
	filtered_list = []
	gnmap_loc = ipaddr + "/" + ipaddr + ".gnmap"
	with open(gnmap_loc, 'r') as f:
		contents = f.read().split(" ")
		r = re.compile(r"\d+/\D+/\D+//")
		filtered_list = list(filter(r.search, contents))
		for entry in filtered_list:
			for protocol in web_check:
				if protocol in entry:
					search_list.append(entry)
		for filtered_entry in search_list:
			r2 = re.match(r"\d+", filtered_entry)
			if r2.group(0) == '80':
				enum(ipaddr, r2.group(0), "http://" + ipaddr).run_ferox_http()
				enum(ipaddr, r2.group(0), "http://" + ipaddr).run_nikto()
			elif r2.group(0) == '443':
				enum(ipaddr, r2.group(0), "https://" + ipaddr).run_ferox_https()
				enum(ipaddr, r2.group(0), "https://" + ipaddr).run_nikto()
			elif "https" in filtered_entry:
				enum(ipaddr, r2.group(0), "https://" + ipaddr).run_ferox_https()
				enum(ipaddr, r2.group(0), "https://" + ipaddr).run_nikto()
			elif "http" in filtered_entry:
				enum(ipaddr, r2.group(0), "http://" + ipaddr).run_ferox_http()	
				enum(ipaddr, r2.group(0), "http://" + ipaddr).run_nikto()



def main():
	try:
		args = get_arguments()
		system_list = handle_file(args.file_list)
		for line in system_list:
			web_enum = enum(line).run_nmap()
			if args.web_enum:
				determine_if_http(line)
	except KeyboardInterrupt:
		print(red + "\n[-]" + reset + " Ctrl + C detected, exiting now.")
	except FileExistsError:
		print(red + "\n[-]" + reset + " The folder" + red +  f" {line} " + reset + "already exists, either delete or rename this folder to prevent overwriting.")


if __name__ == "__main__":
	main()

















