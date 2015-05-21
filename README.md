# mapreduce-logs-consolidator
consolidates all logs from all tasks of Hadoop Job to a single file.

This code is based on SO thread: http://stackoverflow.com/questions/18518983/consolidate-mapreduce-logs

Thanks to @FuriousGeorge for his initiation.

This code in Python gathers all logs from all tasks (of hadoop job) to a single log file!
Actually there are 2 files: one for mappers and one for reducers.
In order to use it, you need to install Python 3 (NOTE: python 3!) on the machine that you run the script from. For example, I can run the script from my desktop, and direct it to collect the logs from my VCD. In this case, I need Python on my desktop.

To run the script:
The name of the script consolidator.py
arg1: job-id
arg2: base URL of job tracker

>python consolidator.py job_201504300451_0065 http://vbox.localdomain:50030/

Note that in the hadoop task’s logs there are several sections: stdout, stderr and syslog. The script takes all 3 parts, and gathers them.

Another note: this code is dependent on "Beautiful Soup" package. http://www.crummy.com/software/BeautifulSoup/bs4/doc/




