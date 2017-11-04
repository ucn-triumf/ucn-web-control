#!/bin/tcsh

# Script that calls other end of run scripts.

# Update runlog 
/home/ucn/online/ucn-web-control/create_runlog.py


# midas2root converter
/home/ucn/online/ucn_detector_analyzer/midas2root_eor.csh

