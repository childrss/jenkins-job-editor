#!/usr/bin/python
# -*- coding: utf-8 -*-

# M@ Childress Oct 2016
# Script to walk Jenkins jobs, find config.xml files 
# and change the command
#
# ! Caveat: this is a very rudimentary script that is likely
# to break in future MSC releases. Use at your own risk

import fileinput
import re
import plistlib
import os
from os.path import isfile, isdir, join, getmtime
import datetime as dt
from xml.etree import ElementTree

jenkinsjobsdir="/Users/Shared/Jenkins/Home/jobs"
jenkinsjobsdir= os.path.normpath(jenkinsjobsdir)
filename="config.xml"
res = []
loop_counter=1

# How many levels deep to go.  Zero=infinate
max_depth=1	

# This is the full bit of the command -- it should be parsed better than the code I'm going to do
# this code assumes that it is a bare-bones formatted "autopkg run recipe" command:
#      <command>/usr/local/bin/autopkg run GoogleChrome.munki.recipe</command>
#
# new command #      <command>/usr/local/bin/autopkg run -v --post &quot;io.github.hjuutilainen.VirusTotalAnalyzer/VirusTotalAnalyzer&quot; GeoGebra.munki.recipe</command>

replacement_command="/usr/local/bin/autopkg run -v --post \"io.github.hjuutilainen.VirusTotalAnalyzer/VirusTotalAnalyzer\" "

# topdown option is required in order to be able to manipulate the directory list (to set depth)
for root, dirs, filenames in os.walk(jenkinsjobsdir, topdown=True):
    depth = root[len(jenkinsjobsdir) + len(os.path.sep):].count(os.path.sep)
    print "max_depth=", max_depth, " depth=",  depth
    if depth == max_depth:
    	res += [os.path.join(root, d) for d in dirs]
    	dirs[:] = [] # Don't recurse any deeper
    	filenames[:] = [] # Don't process the files here, as they're past max_depth
    # print "res=", res
    # print "dirs=", dirs
    # print "filenames=", filenames
    # print "loop # =", loop_counter
    print "-------------------"
    print
    loop_counter += 1
    for filename in filenames:
        if filename == "config.xml": 
        
           # we've found the config file, we don't need any other files or directories in this branch
     	   dirs[:] = [] # Don't recurse any deeper
    	   filenames[:] = [] # Don't process the files here, as they're past max_depth
    	   
           config_xml_to_edit = (join(root, filename))
           print config_xml_to_edit
           file_pointer = open( config_xml_to_edit,'r')
           config_xml_data = file_pointer.read()
           file_pointer.close()  # close the file
           command = re.findall(r'<command>(.*?)</command>',config_xml_data)
           
           try:
           		command = command[0] # take the first element from the findall array and make it into a string
           except:
           		break
           # print '%s does not exist, so can\'t be read' % filename
           # print '\nThe plist full contents is %s\n' % config_xml_data
           if "autopkg" in command:  # lets make sure it's an autopkg jenkins job
               # Now lets split the command string into arguments
               # this HELPS to make sure it is a simple 3-element autopkg command in the form 
               # autopkg -run name-of-recipe-to-run
               command=command.split()
               command_length = len(command)
               if ( command_length == 3 ):  
                   new_command = replacement_command + command[2]
                   print new_command
                   replace_new_command = "\n     <command>" + new_command + "</command>"
                   config_xml_data = re.sub(r'\s*(<command>).*?(</command>)', replace_new_command, config_xml_data)
                   # print config_xml_data
                   # file_pointer = open( config_xml_to_edit, 'w')
                   # file_pointer.write(config_xml_data)
                   # file_pointer.close()
                   print
# print(res)