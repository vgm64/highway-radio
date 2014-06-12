
import MySQLdb
import numpy as np

contours_filename = '/Users/mwoods/Work/OldJobs/Insight/Radio/highway-radio/raw_data/fcc/FM_service_contour_current.txt'
contours_file = open(contours_filename)

def get_database_conn():
  connection = MySQLdb.connect('localhost', 'root', '', 'insight')
  cursor = connection.cursor()
  return connection, cursor

def clean():
  pass

def message():
  pass

def insert_into_msqyl(data, reset=True):
  connection = MySQLdb.connect('localhost', 'root', '', 'insight')
  with connection:
    cursor = connection.cursor()
    if reset:
      cursor.execute("DROP TABLE IF EXISTS contours;")
      cursor.execute("CREATE TABLE contours (id INT PRIMARY KEY AUTO_INCREMENT, \
        callsign CHAR(50), \
        scs CHAR(50), \
        antlat FLOAT, \
        antlon FLOAT, \
        minlat FLOAT, \
        maxlat FLOAT, \
        minlon FLOAT, \
        maxlon FLOAT, \
        size FLOAT, \
        max_r FLOAT, \
        lats TEXT, \
        lons TEXT)")
    base_query = """INSERT INTO contours (callsign, scs, antlat, antlon, minlat, maxlat, minlon, maxlon, size, max_r, lats, lons) VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    print "Entering execute for loop"
    for i, datum in enumerate(data):
      if i%100 == 0:
        print i, 'of', len(data), 'with contour length', len(data[i][-1])
      cursor.execute(base_query, datum)
    #cursor.executemany(base_query, data)
    #connection.commit()

def area_of_polygon(x, y):        
    # Via
    # http://stackoverflow.com/questions/451426/how-do-i-calculate-the-surface-area-of-a-2d-polygon
    x = np.asanyarray(x)
    y = np.asanyarray(y)
    n = len(x)
    shift_up = np.arange(-n+1, 1)
    shift_down = np.arange(-1, n-1)    
    return (x * (y.take(shift_up) - y.take(shift_down))).sum() / 2.0

def calc_contour_topology(antenna, lats, lons):
  lats = np.array(lats)
  lons = np.array(lons)
  area = area_of_polygon(lats, lons)
  max_r = np.hypot(lats - antenna[0], lons - antenna[1]).max()
  return lats.min(), lats.max(), lons.min(), lons.max(), area, max_r


if __name__ == '__main__':
  i = 0
  data_holder = []
  #connection, cursor = get_database_conn()
  # Start a loop over lines in the file.
  # Each line is a radio station (or antenna?)
  print "Working on parsing contour lines"
  for line in contours_file:
    contour_data = []
    # Get some of the identifiers.
    fields = line.split("|")
    uniq_id = fields.pop(0).strip()
    band = fields.pop(0).strip()
    call_sign = fields.pop(0).strip()
    call_sign = call_sign.split(' ')[0]
    scs = call_sign.split('-')[0] # Short call sign.
    antenna_latlon = fields.pop(0).strip()
    antenna_latlon = np.fromstring(antenna_latlon, sep=',')
    # Remove ^\n at the end
    fields.pop()

    # This is kind of a weird way of separating lat and lon, but it turns out
    # that is it is ~5x faster.
    latlon = ','.join(fields)
    # Remove erroneous spaces.. just for looks.
    latlon = latlon.replace(' ', '')
    latlon = latlon.split(',') 
    lats = ','.join(latlon[::2])
    lons = ','.join(latlon[1::2])
    #arr_lats = np.array(lats).astype(np.float32)
    #arr_lons = np.array(lons).astype(np.float32)
    arr_lats = np.fromstring(lats, sep=',')
    arr_lons = np.fromstring(lons, sep=',')
    min_lat, max_lat, min_lon, max_lon, contour_size, max_r = \
        calc_contour_topology(antenna_latlon, arr_lats, arr_lons)
    contour_data.append(call_sign)
    contour_data.append(scs)
    contour_data.append(antenna_latlon[0])
    contour_data.append(antenna_latlon[1])
    contour_data.append(min_lat)
    contour_data.append(max_lat)
    contour_data.append(min_lon)
    contour_data.append(max_lon)
    contour_data.append(contour_size)
    contour_data.append(max_r)
    contour_data.append(lats)
    contour_data.append(lons)
    data_holder.append(contour_data)
    i += 1
    #if i > 1000:
      #break
  print 'Inserting into mysql'
  insert_into_msqyl(data_holder)

    
  


