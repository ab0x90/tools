# README for Ipgeo

## A python program for analyzing web responses for missing headers

This program can take a list of URLs from a file(one per line) or a single URL as input.

Usage:
```sh
pip3 install -r requirements.txt
python3 web_headers.py -h
```

Example commands:
```sh
python3 web_headers.py -f list.txt
python3 web_headers.py -u https://www.google.com 
```


```sh
python3 web_headers.py -h
Usage: web_headers.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILE_LIST, --file_list=FILE_LIST
                        File with a list of URLs
  -u URL, --url=URL     Enter a single URL
```

Example Output:

![](1.png)