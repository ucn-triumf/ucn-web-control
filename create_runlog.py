#!/usr/bin/python
import sys
import json
import time
import os
import math
import fileinput

"""
This class deals with populating the runlog.txt file with a summary of each run.

T. Lindner
Aug 2017

Script adapted from examples from Lars Martin and Tom Feusels
"""


class runlog:



  def initialize_files(self, htmlfile,txtfile):
    htmlfile.write(
        "<!DOCTYPE html>\n "
        " <html>\n "
        "\n"
        "<head>\n"
	"<meta http-equiv='refresh' content='60'>\n "
        "<style>\n"
        "table {\n"
        "    width:100%;\n"
        "}\n"
        "table, th, td {\n"
        "    border: 1px solid black;\n"
        "    border-collapse: collapse;\n"
        "}\n"
        " th, td {\n"
        "    padding: 5px;\n"
        "    text-align: left;\n"
        "}\n"
        "table#nicetable tr:nth-child(even) {\n"
        "    background-color: #eee;\n"
        "}\n"
        "table#t01 tr:nth-child(odd) {\n"
        "   background-color:#fff;\n"
        "}\n"
        "table#nicetable th{\n"
        "    background-color: black;\n"
        "    color: white;\n"
        "}\n"
        "</style>\n"
        "</head>\n"
        "\n"
        "<body>\n"        
        )

    htmlfile.write('<table id="nicetable">\n')
    #htmlfile.write('<tr> <td> Run Number </td>  <td> Start </td> <td> End Time </td>\n')
    htmlfile.write('<tr> <td> Run </td>  <td> Start </td>\n')
    htmlfile.write('<td> <pre> Beamline \n enabled?</pre> </td> \n')
    htmlfile.write('<td> <pre> Beam on \n time (s)</pre> </td> \n')
    htmlfile.write('<td> <pre> UCN Valve \n open (s)</pre> </td> \n')
    htmlfile.write('<td> He-3 \n events </td>  <td> Li-6 \n events </td> <td> UCN Experiment </td><td> Shifters </td> <td> Comments </td> </tr>\n')
    
    txtfile.write("Run number, Start Time, Beamline enabled?, Beam on time, UCN Valve Open, ")
    txtfile.write("He-3 events, Li-6 events, UCN Experiment, Shifter, Comments")
    return

  def writecolumn(self,htmlfile,txtfile,value):

    htmlfile.write("<td>" + value + "</td>");
    txtfile.write(value + ", ");

  def odb2html(self, odb, htmlfile,txtfile):
    # Run number / data logged flag / Start time / EBuilder events / Fragment list / comments
    run_number = odb['Runinfo']['Run number']
    start_time = odb['Runinfo']['Start time']
    stop_time = odb['Runinfo']['Stop time']
    beamline_enabled = "no"
    if odb['Equipment']['BeamlineEpics']['Variables']['Measured'][1] and odb['Equipment']['BeamlineEpics']['Variables']['Measured'][3]:
        beamline_enabled = "yes"

    beamon_time = odb['Equipment']['BeamlineEpics']['Variables']['Measured'][30] *0.000888111
    valveopen_time = odb['Equipment']['UCNSequencer']['Settings']['valveOpenTime']
    he3_events = 0
    li6_events = 0
    if 'V785' in odb['Equipment']:
      he3_events = odb['Equipment']['FEV785']['Statistics']['Events sent']
    elif 'V1725_Slow' in odb['Equipment']:
      if 'TUC0' in odb['Equipment']['V1725_Slow']['Variables']:
        he3_events = odb['Equipment']['V1725_Slow']['Variables']['TUC0'][1]    
    else:
      he3_events = odb['Equipment']['HE3_Detector']['Statistics']['Events sent']
    if 'FEV1720I' in odb['Equipment']:
      li6_events = odb['Equipment']['FEV1720I']['Statistics']['Events sent']
    elif 'V1725_Slow' in odb['Equipment']:
      if 'TUC0' in odb['Equipment']['V1725_Slow']['Variables']:
        li6_events = odb['Equipment']['V1725_Slow']['Variables']['TUC0'][0]    
    else:
      li6_events = odb['Equipment']['Li6_Detector']['Statistics']['Events sent']

    comment = "*NO COMMENT FIELD*"
    ucn_experiment = ""
    shifters = ""
    if "Edit on start" in odb['Experiment']:
      comment = odb['Experiment']['Edit on start']['Comment']
      if "Experiment number" in odb['Experiment']['Edit on start']:
        ucn_experiment = odb['Experiment']['Edit on start']['Experiment number']
      if "Shifters" in odb['Experiment']['Edit on start']:
        shifters = odb['Experiment']['Edit on start']['Shifters']

    htmlfile.write("<tr>")
    self.writecolumn(htmlfile,txtfile,str(run_number))
    self.writecolumn(htmlfile,txtfile,str(start_time))
    #self.writecolumn(htmlfile,txtfile,str(stop_time))
    self.writecolumn(htmlfile,txtfile,beamline_enabled)
    self.writecolumn(htmlfile,txtfile,str(round(beamon_time,2)))
    self.writecolumn(htmlfile,txtfile,str(valveopen_time))
    self.writecolumn(htmlfile,txtfile,str(he3_events))
    self.writecolumn(htmlfile,txtfile,str(li6_events))
    self.writecolumn(htmlfile,txtfile,ucn_experiment)
    self.writecolumn(htmlfile,txtfile,shifters)
    self.writecolumn(htmlfile,txtfile,comment)
    htmlfile.write("</tr>\n")

    txtfile.write("\n")


    

    return

  def odbFromJson(self, filename):
    with open(filename, "r") as file:
      data = file.read()
      odb = json.loads(data, "ISO-8859-1")
      return odb


  def bulkupload(self):

    htmlfile = open('/home/ucn/online/ucn-web-control/runlist.html','w')
    txtfile = open('/home/ucn/online/ucn-web-control/runlist.txt','w')
    self.initialize_files(htmlfile,txtfile)


    seen_datadirs = []
    data_dir = "/data/ucn/midas_files/"
    print "done"
    os.chdir(data_dir)
    print "done2"
    for filename in reversed(sorted(os.listdir(data_dir))):
      if (filename.find("json") == -1):
        continue

      odb = self.odbFromJson(filename)
      print odb['Runinfo']['Run number']
      print filename
      

      self.odb2html(odb,htmlfile,txtfile)

    htmlfile.write('</table>\n')
    htmlfile.write("</body>\n"
                  "</html>\n")


  def dummy(self):
    print "Dummy function"

if __name__ == "__main__":
  runlog().bulkupload()
