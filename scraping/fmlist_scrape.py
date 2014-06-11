""" Running this script will scrape data from a radio attena database website.
The raw HTML will be stored and parsed later.
"""

import urllib2
import urllib3
import time
import random



WEBSITE = "http://www.fmlist.org/ul_ukwliste.php?itu=USA&recent=&clToSort=frequency&startValue={0}&nrOfValues={1}&lastClicked=frequency&selected=1"
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

def sleep_randomly(sleep_min, sleep_max=None):
  t = None
  if sleep_max:
    t = random.random()*(sleep_max - sleep_min) + sleep_min
  else:
    t = randdom.random()*sleep_min
  time.sleep(t)
  return t


""" NOT REALLY USED.... """
def scrape_fmlist(pool, start, num_records, outpath='./'):
  pool = urllib3.HTTPConnectionPool()
  url = WEBSITE.format(start, num_records)
  resp = pool.request('GET', url, headers=HEADER)
  filename = '%s/fmlist_%06d_%04d.html' % (outpath, start, num_records)
  out_filename = outpath
  #with open(outpath, 'w') as out_file:
    #out_file.write(resp.




if __name__ == '__main__':
  print 'Main'
  outpath = '/Users/mwoods/Work/OldJobs/Insight/Radio/highway-radio/raw_data/fmlist'
  pool = urllib3.connection_from_url('http://www.fmlist.org')
  start_record = 1
  num_records_per_request = 100
  total_num_records = 17725 # Looked at their webpage
  for start in range(start_record, total_num_records, num_records_per_request):
    print 'Scraping records', start, 'through', start + num_records_per_request
    start_time = time.time()

    url = WEBSITE.format(start, num_records_per_request)
    #print url
    #class BAH:
      #def __init__(self):
        #self.data = 'hi'
    #resp = BAH()
    resp = pool.request('GET', url, headers=HEADER)

    filename = '%s/fmlist_%06d_%04d.html' % (outpath, start, num_records_per_request)
    with open(filename, 'w') as out_file:
      out_file.write(resp.data)

    print 'Read', len(resp.data)/1024, 'kilobytes and wrote to disk. That took', time.time() - start_time, 'seconds.'
    sleep_time = sleep_randomly(sleep_min = 2, sleep_max = 6)
    print 'Querying again after', sleep_time, 'seconds of sleep.'
    print ''

