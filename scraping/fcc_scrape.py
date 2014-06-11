"""
FCC SCRAPER!!!

Running this script will scrape data from the fcc radio tower website.
The raw HTML will be stored and parsed later.
"""

CURRENT_HASH = '0'
#CURRENT_HASH = '1'
#CURRENT_HASH = '2'
#CURRENT_HASH = '3'
#CURRENT_HASH = '4'
#CURRENT_HASH = '5'
#CURRENT_HASH = '6'
#CURRENT_HASH = '7'
#CURRENT_HASH = '8'
#CURRENT_HASH = '9'
#CURRENT_HASH = 'a'
#CURRENT_HASH = 'b'
#CURRENT_HASH = 'c'
#CURRENT_HASH = 'd'
#CURRENT_HASH = 'e'
#CURRENT_HASH = 'f'


import urllib2
import urllib3
import time
import random
import MySQLdb
from md5 import md5



WEBSITE = "http://transition.fcc.gov/fcc-bin/fmq?state=&call={}&city=&arn=&serv=&vac=&freq=0.0&fre2=107.9&facid=&asrn=&class=&dkt=&list=1&dist=&dlat2=&mlat2=&slat2=&NS=N&dlon2=&mlon2=&slon2=&EW=W&size=9"
HEADER = {
'Host': 'transition.fcc.gov',
'Connection': 'keep-alive',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
'Accept-Encoding': 'gzip,deflate,sdch',
'Accept-Language': 'en-US,en;q=0.8',
}

def sleep_randomly(sleep_min, sleep_max=None):
  t = None
  if sleep_max:
    t = random.random()*(sleep_max - sleep_min) + sleep_min
  else:
    t = randdom.random()*sleep_min
  time.sleep(t)
  return t

def get_database_conn():
  connection = MySQLdb.connect('localhost', 'root', '', 'insight')
  cursor = connection.cursor()
  return connection, cursor

def get_callsigns():
  connection, cursor = get_database_conn()
  cursor.execute("SELECT DISTINCT program FROM fmlist WHERE program IS NOT NULL")
  result = cursor.fetchall()
  call_signs = []
  for call_sign in result:
    # W299AS r:WKCB ---> W299AS
    new_call_sign = call_sign[0].split()[0]
    # WCLN-FM ---> WCLN
    new_call_sign = new_call_sign.replace("-LP", "")
    call_signs.append(new_call_sign)
  return call_signs


if __name__ == '__main__':
  print 'Main'
  outpath = '/Users/mwoods/Work/OldJobs/Insight/Radio/highway-radio/raw_data/fcc'
  pool = urllib3.connection_from_url('http://transition.fcc.gov')

  list_of_callsigns = get_callsigns()
  # To make this more do-able over a few days, only do some queries. Separate
  # them by hash.
  hash_dict = {}
  for call_sign in list_of_callsigns:
    hash_dict[call_sign] = md5(call_sign).hexdigest()[0]
  # DEBUGGING
  #list_of_callsigns = list_of_callsigns[:2]
  #print "Trying to query for:", list_of_callsigns

  for call_sign in list_of_callsigns:
    if hash_dict[call_sign] != CURRENT_HASH:
      print "## Skipping", call_sign, 'based on hash separation'
      continue
    print '>> Scraping FCC listined for', call_sign
    start_time = time.time()
    url = WEBSITE.format(call_sign)
    resp = pool.request('GET', url, headers=HEADER)

    filename = '{}/fcc_{}.html'.format(outpath, call_sign)
    with open(filename, 'w') as out_file:
      out_file.write(resp.data)
    print '>> Read', len(resp.data)/1024, 'kilobytes and wrote to disk. That took',
    print time.time() - start_time, 'seconds.'
    sleep_time = sleep_randomly(sleep_min = 2, sleep_max = 4)
    print '>> Querying again after', sleep_time, 'seconds of sleep.'
    print ''
