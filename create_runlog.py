#!/usr/bin/python
import sys
import json
import time
import os
import math
import fileinput

"""
This class deals with populating the runlog.txt file with a summary of each run.
"""


class runlog:



  def initialize_html(self, outfile):
    outfile.write(
        "<!DOCTYPE html>\n "
        " <html>\n "
        "\n"
        "<head>\n"
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

    outfile.write('<table id="nicetable">\n')
    outfile.write('<tr> <td> Run Number </td>  <td> Start Time </td> <td> End Time </td>">\n')
    outfile.write('<td> He-3 events </td>  <td> Li-6 events </td> <td> Comments </td> </tr>">\n')
    return

  def odb2html(self, odb, outfile):
    # Run number / data logged flag / Start time / EBuilder events / Fragment list / comments
    run_number = odb['Runinfo']['Run number']
    start_time = odb['Runinfo']['Start time']
    stop_time = odb['Runinfo']['Stop time']
    he3_events = odb['Equipment']['FEV785']['Statistics']['Events sent']
    li6_events = odb['Equipment']['FEV1720I']['Statistics']['Events sent']

    comment = "*NO COMMENT FIELD*"
    if "Edit on start" in odb['Experiment']:
      comment = odb['Experiment']['Edit on start']['Comment']

    txt = "<tr>"
    txt += "<td>" + str(run_number).rjust(7) + "</td>"
    txt += "<td>" + str(start_time).ljust(27) + "</td>"
    txt += "<td>" + str(stop_time).ljust(27) + "</td>"
    txt += "<td>" + str(he3_events) + "</td>"
    txt += "<td>" + str(li6_events) + "</td>"
    txt += "<td>" + comment + "</td>"
    txt += "</tr>"
    outfile.write(txt + "\n");
    return txt

  def odbFromJson(self, filename):
    with open(filename, "r") as file:
      data = file.read()
      odb = json.loads(data, "ISO-8859-1")
      return odb


  def bulkupload(self):

    outfile = open('/home/ucn/online/ucn-web-control/runlist.html','w')
    self.initialize_html(outfile)


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
      

      self.odb2html(odb,outfile)

    outfile.write('</table>\n')
    outfile.write("</body>\n"
                  "</html>\n")


  def dummy(self):
    print "Dummy function"

if __name__ == "__main__":
  runlog().bulkupload()
