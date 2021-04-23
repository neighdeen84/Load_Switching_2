#! /usr/bin/python3
import argparse
import os
import csv
import datetime as dt
from dateutil.parser import parse as date_parse
parser = argparse.ArgumentParser(description='Simulate NeoCharge output with two loads')
parser.add_argument('primary_source_file', help="file to read primary load from")
parser.add_argument('secondary_source_file', help="file to read secondary load from")
parser.add_argument('dest_file', help='file to write simulated load to')
parser.add_argument("-f", "--force", action="store_true", help="force overwrite of existing destination file")
parser.add_argument("-v", "--verbose", action="store_true", help="add extra columns for debugging")
args = parser.parse_args()

primary_source_ext = os.path.splitext(args.primary_source_file)[-1].lower()
if os.path.isfile(args.primary_source_file):
    print("using: " + args.primary_source_file)
    if primary_source_ext == '.csv':
        print(primary_source_ext + " is supported input")
    else:
        print(primary_source_ext + " not supported use .csv file for input")
        exit()
else:
    print(args.primary_source_file + " not found")
    exit()

secondary_source_ext = os.path.splitext(args.secondary_source_file)[-1].lower()
if os.path.isfile(args.secondary_source_file):
    print("using: " + args.secondary_source_file)
    if secondary_source_ext == '.csv':
        print(secondary_source_ext + " is supported input")
    else:
        print(secondary_source_ext + " not supported use .csv file for input")
        exit()
else:
    print(args.secondary_source_file + " not found")
    exit()

dest_ext = os.path.splitext(args.dest_file)[-1].lower()
if os.path.isfile(args.dest_file):
    if not args.force:
        print("destination file exists use --force to overwrite")
        exit()
    else:
        if dest_ext == '.csv':
            print(dest_ext + " is supported output")
        else:
            print(dest_ext + " not supported use .csv file for output")
            exit()
else:
    if dest_ext == '.csv':
        print(dest_ext + " is supported output")
    else:
        print(dest_ext + " not supported use .csv file for output")
        exit()
    print("creating: ", args.dest_file)

primary_infilename = args.primary_source_file
secondary_infilename = args.secondary_source_file
outfilename = args.dest_file

in_p_CSV = open(primary_infilename, newline='')
in_s_CSV = open(secondary_infilename, newline='')
filter_col = ['None','topic']
outCSV = open(outfilename, 'w', newline='')
primary_reader = csv.DictReader(in_p_CSV, fieldnames=['time','watts'])
secondary_reader = csv.DictReader(in_s_CSV, fieldnames=['time','watts'])
if args.verbose:
    fields = list(['time','timestamp','p','s','switched','state','change','secondary_time'])
else:
    fields = list(['time','switched'])
writer = csv.DictWriter(outCSV, fieldnames=fields, dialect='excel')
if args.verbose:
    writer.writeheader()

states_list = ['primary','primary_on','primary_off','secondary']
# states_dict = {'primary':0 ,'primary_on':1 ,'primary_off':2 ,'secondary':3}
#FIXME if primary is on in first timestamp how is that handled
previous_state = 'secondary'
state = ''
#FIXME initialize with time objects
primary_on_time = ''
primary_off_time = ''
change = False

#Magic goes here
next_primary = next(primary_reader)
next_secondary = next(secondary_reader)
while next_primary:
    time = date_parse(next_primary['time'])
    secondary_time = date_parse(next_secondary['time'])
    # don't copy rows of wrong message type
    row = { 'time':next_primary['time'],'timestamp':time.timestamp(), 'p':next_primary['watts'], 's':0 }
    if float(next_primary['watts']) > 99:
#        print("over_99")
        if previous_state == 'secondary':
#            print('state changed from secondary to primary_on')
            change = True
            state = 'primary_on'
            previous_state = 'primary_on'
            primary_on_time = time
        elif previous_state == 'primary_on':
            on_time = (time - primary_on_time).total_seconds()
            if on_time >= 3:
#                print('state changed from primary_on to primary')
                change = True
                state = 'primary'
                previous_state = 'primary'
                #set time to something that will make errors obvious
                primary_on_time = dt.date(1970,1,1)
            else:
                state = 'primary_on'
                previous_state = 'primary_on'
                #set time to something that will make errors obvious
                primary_off_time = dt.date(1970,1,1)
        elif previous_state == 'primary_off':
#            print('state changed from primary_off to primary')
            change = True
            state = 'primary'
            previous_state = 'primary'
        # only possibility left is 'primary'
        else:
            state = 'primary'
            previous_state = 'primary'
    # below 99 watts
    else:
        if previous_state == 'primary':
#            print('state changed from primary to primary_off')
            change = True
            state = 'primary_off'
            previous_state = 'primary_off'
            primary_off_time = time
        elif previous_state == 'primary_off':
            off_time = (time - primary_off_time).total_seconds()
            off_wait_time = 60 + 23 # 1:23
            if off_time >= off_wait_time:
#                print('state changed from primary_off to secondary')
                change = True
                state = 'secondary'
                previous_state = 'secondary'
                off_time = dt.date(1970,1,1)
            else:
                state = 'primary_off'
                previous_state = 'primary_off'
        elif previous_state == 'primary_on':
            # is the right change to primary_off?
#            print('state changed from primary_on to secondary')
            change = True
            state = 'secondary'
            previous_state = 'secondary'
            on_time = dt.date(1970,1,1)
        # only state left is it was already secondary
        else:
            state = 'secondary'
            previous_state = 'secondary'
    if state == 'primary_on' or state == 'secondary':
        # replace 0 in 's' column with data from secondary csv
        row['s'] = next_secondary['watts']
        secondary_time = date_parse(next_secondary['time'])
        row['secondary_time'] = secondary_time
        while True:
            # load next value from secondary CSV or False if on last line
            next_secondary = next(secondary_reader,False)
            if not next_secondary:
                break
            secondary_time = date_parse(next_secondary['time'])
            secondary_watts = next_secondary['watts']
            if float(secondary_watts) > 99:
                break
            if secondary_time > time:
                break
    row['state'] = state
    row['change'] = change
    row['switched'] = float(row['p']) + float(row['s'])
    if args.verbose:
        writer.writerow(row)
    else:
        rowcopy = {'time':row['time'],'switched':row['switched'] }
        writer.writerow(rowcopy)
#    print(state)
    # prepare for next loop
    change = False
    # if no next row instead set next_primary to False
    next_primary = next(primary_reader,False)

