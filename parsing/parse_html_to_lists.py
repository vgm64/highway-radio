
from bs4 import BeautifulSoup
import re
import MySQLdb


def open_html(filename):
  infile = open(filename)
  raw_text = infile.read()
  # I don't know where, but SOMEWHERE this onmousedown or ondblclick totally
  # fucks up parsing.
  raw_text = re.sub('onmousedown=".*?"', '', raw_text)
  raw_text = re.sub('ondblclick=".*?"', '', raw_text)
  soup = BeautifulSoup(raw_text)
  return soup

def yield_rows(soup):
  for tr in soup.table.find_all('tr')[1:]:
    yield tr

def parse_row(row):
  results = []
  for item in row.find_all('td'):
    #print item.contents, '----', item
    if len(item.contents) > 0:
      results.append(item.contents[0].encode('ascii', 'ignore'))
    else:
      results.append(None)
  #print '@@@', results
  return results


def parse_html_to_lists(filename):
  soup = open_html(filename)
  row_iterator = yield_rows(soup)
  #td_iterator = yield_tds(soup)

  heading = 'frequency p location  reg la  program regprogram  pty mod power dir pol height  coord ant haat  rds_id  rds_reg pi_id pi_reg  remarks powertrp'
  all_results = []
  for row in row_iterator:
    results = parse_row(row)
    all_results.append(results)
  return all_results

def get_database_conn():
  connection = MySQLdb.connect('localhost', 'root', '', 'insight')
  cursor = connection.cursor()
  return connection, cursor

def insert_into_msqyl(data, reset=True):
  connection = MySQLdb.connect('localhost', 'root', '', 'insight')
  with connection:
    cursor = connection.cursor()
    if reset:
      cursor.execute("DROP TABLE IF EXISTS fmlist;")
      cursor.execute("CREATE TABLE fmlist (id INT PRIMARY KEY AUTO_INCREMENT, \
        frequency FLOAT, \
        p CHAR(10), \
        location CHAR(100), \
        reg CHAR(50), \
        la CHAR(50), \
        program CHAR(50), \
        regprogram CHAR(100), \
        pty CHAR(100), \
        modmod CHAR(100), \
        power FLOAT, \
        dir CHAR(50), \
        pol CHAR(50), \
        height FLOAT, \
        coord CHAR(50), \
        ant CHAR(50), \
        haat CHAR(50), \
        rds_id CHAR(100), \
        rds_reg CHAR(50), \
        pi_id CHAR(50), \
        pi_reg CHAR(50), \
        remarks CHAR(50), \
        powertrp CHAR(50), \
        cat CHAR(100), \
        lat FLOAT, \
        lon FLOAT)")
    base_query = """INSERT INTO fmlist (frequency, p, location,  reg, la, program, regprogram, pty, modmod, power, dir, pol, height, coord, ant, haat, rds_id, rds_reg, pi_id, pi_reg, remarks, powertrp, cat, lat, lon) VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    #print "Entering execute for loop"
    #for datum in data:
      #print datum
      #cursor.execute(base_query, datum)
    cursor.executemany(base_query, data)
    connection.commit()
  
def clean(data):
  for antenna_record in data:
    # Remove a stray newline.
    antenna_record.pop(-1)

    # Tweak call_sign.
    call_sign = antenna_record[5]
    if not call_sign:
      call_sign = 'XXXX'
    call_sign = call_sign.split(' ')[0]
    antenna_record[5] = call_sign 

    # Tweak categories
    remark = antenna_record[-2]
    remark = category_swap(remark, 'Spanis', 'Spanish')
    remark = category_swap(remark, 'Jaz', 'Jazz')
    remark = category_swap(remark, '80', '80s')
    remark = category_swap(remark, '90', '90s')
    remark = category_swap(remark, 'Adult', 'Adult Contemporary')
    remark = category_swap(remark, 'Altern', 'Alternative')
    remark = category_swap(remark, 'CHR', 'Top Hits')
    remark = category_swap(remark, 'Christ', 'Christian')
    remark = category_swap(remark, 'Classi', 'Classical')
    remark = category_swap(remark, 'Colleg', 'College Radio')
    remark = category_swap(remark, 'commun', 'Community Radio')
    remark = category_swap(remark, 'Commun', 'Community Radio')
    remark = category_swap(remark, 'Countr', 'Country')
    remark = category_swap(remark, 'Contem', 'Top Hits')
    remark = category_swap(remark, 'dance', 'Dance')
    remark = category_swap(remark, 'Eclect', 'Eclectic')
    remark = category_swap(remark, 'Hot AC', 'Adult Contemporary')
    remark = category_swap(remark, 'High S', 'High School Radio')
    remark = category_swap(remark, 'Hip Ho', 'Hip Hop')
    remark = category_swap(remark, 'News', 'News')
    remark = category_swap(remark, 'NPR', 'News')
    remark = category_swap(remark, 'Region', 'Regional Mexican')
    remark = category_swap(remark, 'Relig', 'Religious')
    remark = category_swap(remark, 'Rhyth', 'Top Hits')
    remark = category_swap(remark, 'Smoot', 'Jazz')
    remark = category_swap(remark, 'Soft A', 'Adult Contemporary')
    remark = category_swap(remark, 'Soft R', 'Rock')
    remark = category_swap(remark, 'South', 'Gospel')
    remark = category_swap(remark, 'Variet', 'Variety')
    remark = category_swap(remark, 'Top', 'Top Hits')
    remark = category_swap(remark, 'AC', 'Adult Contemporary')
    remark = category_swap(remark, 'AAA', '')
    #if not remark:
      #continue
    #elif 'Spanis' in remark:
      #remark = 'Spanish'
    #elif 'Jaz' in remark:
      #remark = 'Jazz'
    #elif '80' in remark:
    antenna_record.append(remark)
    
  return

def category_swap(partial_category, match_term, return_term):
  if partial_category and match_term in partial_category:
    return return_term
  else:
    return partial_category

def massage(data):
  for antenna_record in data:
    # Add in floating point coordinates.
    coords = antenna_record[13]
    if coords:
      lon,lat = coords.lower().split("/")
      lat = int(lat.split("n")[0]) + float(lat.split("n")[1])/60.
      lon = int(lon.split("w")[0]) + float(lon.split("w")[1])/60.
      lon = -lon
    else:
      lat, lon = None, None
    antenna_record.append(lat)
    antenna_record.append(lon)

  return


if __name__ == '__main__':
  #print "Parsing html"
  #fmlist_data = parse_html_to_lists('/Users/mwoods/Work/OldJobs/Insight/Radio/highway-radio/raw_data/fmlist/fmlist_000001_0100.html')
  #print "Clean data"
  #clean(fmlist_data)
  #print "Massaging data"
  #massage(fmlist_data)
  #print "INserting into db"
  #insert_into_msqyl(fmlist_data)
  #print "Done"

  import glob
  reset_table = True
  for filename in glob.glob('/Users/mwoods/Work/OldJobs/Insight/Radio/highway-radio/raw_data/fmlist/fmlist*.html'):
    print "Working on", filename
    fmlist_data = parse_html_to_lists(filename)
    clean(fmlist_data)
    massage(fmlist_data)
    insert_into_msqyl(fmlist_data, reset_table)
    if reset_table:
      reset_table = False

