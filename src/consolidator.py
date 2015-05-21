#!/usr/bin/python
import sys
from bs4 import BeautifulSoup as BS
from urllib.request import urlopen
#from urllib2 import urlopen
import re
from _winapi import NULL

#TRACKER_BASE_URL = 'http://vbox.localdomain:50030/'
TRACKER_BASE_URL_SUFFIX = 'jobtasks.jsp?jobid=%s&type=%s&pagenum=1'
#TRACKER_URL_FORMAT = TRACKER_BASE_URL + TRACKER_BASE_URL_SUFFIX # use map or reduce for the type

def findLogs(jobtrackerBaseUrl, url):
    finalLog = ""

    print ("Looking for Job: " + url)
    html = urlopen(url).read()
    trackerSoup = BS(html)
    taskURLs = [h.get('href') for h in trackerSoup.find_all(href=re.compile('taskdetails'))]

    # Now that we know where all the tasks are, go find their logs
    logURLs = []
    for taskURL in taskURLs:
        taskHTML = urlopen(jobtrackerBaseUrl + taskURL).read()
        taskSoup = BS(taskHTML)
#        stam = taskSoup.find(href=re.compile('all=true'))
        tasks_urls = taskSoup.find_all(href=re.compile('all=true'))
        for task_url in tasks_urls:
            if(task_url != None):
                allLogURL = task_url.get('href')
#                print ("URL: " + allLogURL)
                logURLs.append(allLogURL)
            else:
                print ("URL is None ")

    print ("********************************")
    # Now fetch the stdout log from each
    for logURL in logURLs:

        #concat the URL to the output:
        finalLog += logURL 
        
        logHTML = urlopen(logURL).read()
#        print ("HTML content: " + logHTML.decode())
        logSoup = BS(logHTML)
#        stdoutText = logSoup.body.pre.text.lstrip()
        preTagsBS = logSoup.find_all('pre')
        #we iterate over the syslog, stderr and stdout
        for preTag in preTagsBS:
#            print (preTag.text)
            finalLog += preTag.text

    return finalLog


def main(argv):
    JobTrackerBaseURL = argv[2]
    trackerURLformat = JobTrackerBaseURL + TRACKER_BASE_URL_SUFFIX  
    with open(argv[1] + "-map-stdout.log", "w") as f:
        f.write( findLogs(JobTrackerBaseURL, trackerURLformat % (argv[1], "map")) )
        print ("Wrote mapers stdouts to " + f.name)

    with open(argv[1] + "-reduce-stdout.log", "w") as f:
        f.write( findLogs(JobTrackerBaseURL, trackerURLformat % (argv[1], "reduce")) )
        print ("Wrote reducer stdouts to " + f.name)

if __name__ == "__main__":
    main(sys.argv)