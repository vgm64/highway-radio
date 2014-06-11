""" Running this script will scrape data from a radio attena database website.
The raw HTML will be stored and parsed later.
"""

import urllib2 as url
import subprocess



CURL_COMMAND = """\
    curl \
    -H "Host: www.fmlist.org" \
    -H "Connection: keep-alive" \
    -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" \
    -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36" \
    -H "Referer: http://www.fmlist.org/ul_ukwliste_menu.php?lastClicked=frequency&selected=3" \
    -H "Accept-Encoding: gzip,deflate,sdch" \
    -H "Accept-Language: en-US,en;q=0.8" \
    -H "Cookie: FMLIST=a87906465d56d11e9716325af7284e1f" \
   'http://www.fmlist.org/ul_ukwliste.php?itu=USA&recent=&clToSort=frequency&startValue=1&nrOfValues=100&lastClicked=frequency&selected=1' """

WEBSITE = "http://www.fmlist.org/ul_ukwliste.php?itu=USA&recent=&clToSort=frequency&startValue=1&nrOfValues=100&lastClicked=frequency&selected=1"
HEADER = {
'Host': 'www.fmlist.org',
'Connection': 'keep-alive',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
'Referer': 'http//www.fmlist.org/ul_ukwliste_menu.php?lastClicked=frequency&selected=3',
'Accept-Encoding': 'gzip,deflate,sdch',
'Accept-Language': 'en-US,en;q=0.8',
'Cookie': 'FMLIST=a87906465d56d11e9716325af7284e1f'
}

import time

#CURL_COMMAND = 'echo hi'
#s1 = time.time()
#proc = subprocess.Popen(CURL_COMMAND, stdout=subprocess.PIPE, shell=True)
#out,err = proc.communicate()
#s2 = time.time()

#print "STDOUT:"
#print out
#print "STDERR:"
#print err

s3 = time.time()
request = url.Request(WEBSITE, headers=HEADER)
res = url.urlopen(request).read()
s4 = time.time()

print "Method 1: Length is", len(out), 'and it took', s2-s1, 'seconds to run'
print "Method 2: Length is", len(res), 'and it took', s4-s3, 'seconds to run'
print out
print '='*80
print res


