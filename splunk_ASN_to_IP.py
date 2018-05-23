#!/usr/bin/python
import splunklib.client as client
import sys
from time import sleep
import splunklib.results as results
from MaltegoTransform import *
import os

HOST = "xxxxxx"
PORT = 8089
USERNAME = "xxxxx"
PASSWORD = "xxxxx"
AS=sys.argv[1] #define in maltego local transform commandline parameter as.number
# Create a Service instance and log in 
service = client.connect(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD)

# Print installed apps to the console to verify login
#for app in service.apps:
#    print app.name

#edit search according to your splunk knowledge objects.
searchquery_normal = "search index=intelmq sourcetype=intelmqJSON source.asn="+ str(AS)+ " |  table source.ip |dedup source.ip | top limit=10 source.ip"

#print searchquery_normal
kwargs_normalsearch = {"exec_mode": "normal"}
job = service.jobs.create(searchquery_normal, **kwargs_normalsearch)

# A normal search returns the job's SID right away, so we need to poll for completion
while True:
    while not job.is_ready():
        pass
    stats = {"isDone": job["isDone"],
             "doneProgress": float(job["doneProgress"])*100,
              "scanCount": int(job["scanCount"]),
              "eventCount": int(job["eventCount"]),
              "resultCount": int(job["resultCount"])}

    status = ("\r%(doneProgress)03.1f%%   %(scanCount)d scanned   "
              "%(eventCount)d matched   %(resultCount)d results") % stats

    #sys.stdout.write(status)
    #sys.stdout.flush()
    if stats["isDone"] == "1":
 
       #sys.stdout.write("\n\nDone!\n\n")
       break
    sleep(2)

reader = results.ResultsReader(job.results())
#for item in reader:
#    print item['source.ip']
#print "Results are a preview: %s" % reader.is_preview


# Get the results and display them
me = MaltegoTransform()
for item in reader:
	#print "-----------------------------------------------"	
	me.addEntity("maltego.IPv4Address",item['source.ip'])
	
me.returnOutput()


job.cancel()   
