import requests 
import optparse
import sys

#get arguments from input
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-l", "--lfi_list", dest="lfi_list", help="lfi list to use for fuzzing")
    parser.add_option("-u", "--url", dest="url", help="URL to fuzz")
    parser.add_option("-f", "--fuzz", dest="fuzz", help="string to input between url and file, example: /../../../../../..")
    (options, arguments) = parser.parse_args()
    if not options.lfi_list:
        parser.error("[-] Please specify a list to use for fuzzing, use --help for more info")
    elif not options.url:
        perser.error("[-] Please specify a URL, use --help for more info")
    return options

def create_variables():
	#variables for lfi fuzz list and url
	lfi_list = options.lfi_list
	url = options.url
	status_code_list = ['200','204','301','302','307','401','403','405']
	return status_code_list, url, lfi_list


#connect to the url and verify its up

def test_url(url):
	print("[+] Attempting to connect to url")
	r = requests.get(url, timeout=3)
	if str(r.status_code) in status_code_list:
		print("[+] Connection attempt successful\n")
		print("*" * 50)
		print("[+] Beginning to fuzz for LFI based on a list\n")


#fuzz for each line in lfi list
def fuzz_time(lfi_list, url, fuzz):
	f = open(lfi_list, "r")
	lines = f.readlines()
	for line in lines:
		line = line.strip()
		r = requests.get(url + fuzz + line, timeout=2)
		if r.text:
			print("[+] Check Here: " + url + fuzz + line)
			#print(r.text)



try: 
	options = get_arguments()
	status_code_list, url, lfi_list = create_variables()
	test_url(options.url)
	fuzz_time(options.lfi_list, options.url, options.fuzz)


except requests.exceptions.RequestException as e:
	print("[-] Failed to connect to the given URL, exiting now")
	sys.exit(0)

