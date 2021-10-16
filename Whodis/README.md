# README for Whodis

## A python program for returning the geolocation and owner of an IP Address/list of IP Addresses

** This program requires an API key from https://ipgeolocation.io/, accounts are free


```sh
python3 whodis.py -h

Usage: whodis.py [options]

Options:
  -h, --help            show this help message and exit
  -i IP_ADDR, --ip_addr=IP_ADDR
                        IP Address to search for
  -f FIELDS, --fields=FIELDS
                        fields to search for, enter a comma seperated list:
                        field,field1,field2
  -c, --csv             output to a csv file
  --lf, --list_fields   list all the possible fields
  -a API_KEY, --api_key=API_KEY
                        Enter your API key
  -F FILE_LIST, --file_list=FILE_LIST
                        Enter your API key
  -n CIDR_NOTATION, --cidr_notation=CIDR_NOTATION
                        Enter an IP Address range using CIDR ex:
                        192.168.1.0/24
  -o OUTPUT_FILE, --output_file=OUTPUT_FILE
                        File name for the csv output, default is
                        whodis_lookup.csv

```


Example commands:
```sh
python3 ip_own.py -a APIKEYHERE -n 192.168.1.0/24 -c 
python3 ip_own.py -a APIKEYHERE -F ip_list.txt -c
python3 ip_own.py -a APIKEYHERE -i 192.168.1.1 -c
```




