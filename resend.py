#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import sys
import subprocess 
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

TEMPLATES_FOLDER = '/templates/'
FILEBEAT_CONFIG = '/filebeat'

def check_mounted_files():
    files = ['/input.log', '/cert.crt']
    
    for file in files:
        if os.path.isfile(file):
            print("{} file is loaded".format(file))
        else:
            sys.exit("{} is not mounted inside the container, please check docker volumen options".format(file))

def ask_input(message):
    yes = {'yes','y', 'ye', ''}
    no = {'no','n'}

    choice = input(message).lower()
    if choice in yes:
        return True
    elif choice in no:
        return False
    else:
        print("Please respond with 'yes' or 'no'")
        sys.exit()

def exec_filebeat():
    cmd  = '/opt/filebeat/filebeat -e -v -c /filebeat.yml -once'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    while proc.poll() is None:
        output = proc.stdout.readline().strip()
        print(output)
    
    output = proc.communicate()[0]
    proc.wait() 

def templates(file_path, template_file, **kwargs):
    jinja = Environment(loader=FileSystemLoader(TEMPLATES_FOLDER),trim_blocks=True)
    content = jinja.get_template(template_file).render(kwargs)

    with open(file_path + '.yml', 'w') as file:
            file.write(content)
    
document_type =  input('Enter the document type: ')
logstash_host =  input('Enter the Logstash host e.g. server.com:5044: ')

if ask_input('Do you want to ingest this log? y/n: '):
    check_mounted_files()
    templates(FILEBEAT_CONFIG, 'filebeat.j2', document_type=document_type, logstash_host=logstash_host)
    exec_filebeat()
