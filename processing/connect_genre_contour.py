""" I have two tables. One has genres. The other, contours. Make a table
to connect the two.
"""

import MySQLdb

def get_database_conn():
  connection = MySQLdb.connect('localhost', 'root', '', 'insight')
  cursor = connection.cursor()
  return connection, cursor

def insert_into_msqyl(data, reset=True):
  connection = MySQLdb.connect('localhost', 'root', '', 'insight')
  with connection:
    cursor = connection.cursor()
    if reset:
      cursor.execute("DROP TABLE IF EXISTS map_fcc_to_fmlist;")
      cursor.execute("CREATE TABLE map_fcc_to_fmlist (id INT PRIMARY KEY AUTO_INCREMENT, \
        fcc_id INT, \
        fmlist_id, \
        )")
    base_query = """INSERT INTO map_fcc_to_fmlist (fcc_id, fmlist_id) VALUES 
    (%s, %s) """
    print "Entering execute for loop"
    for i, datum in enumerate(data):
      if i%100 == 0:
        print i, 'of', len(data)
      cursor.execute(base_query, datum)
    #cursor.executemany(base_query, data)
    #connection.commit()

#def get_fcc_contours

def haversine(lon1, lat1, lon2, lat2):
  """
  Calculate the great circle distance between two points
  on the earth (specified in decimal degrees)
  """
  # convert decimal degrees to radians
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

  # haversine formula
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
  c = 2 * asin(sqrt(a))

  # 6367 km is the radius of the Earth
  km = 3956.27 * c
  return km 

"""
# CALCULATE A GREAT CIRCLE!!
SELECT a.lon , a.lat , b.antlon, b.antlat,
2 * ASIN( 
SQRT( 
    POW( SIN(   (b.antlat - a.lat)/360*2*PI()/2  )  , 2)
    + COS(a.lat/360*2*PI()) 
    * COS(b.antlat/360*2*PI()) 
    * POW(SIN( (b.antlon - a.lon)/360*2*PI()/2), 2)
  )
) * 3956.27 AS geod,
SQRT(POW((a.lat - b.antlat)*75.8, 2) + POW((a.lon - b.antlon)*60,2)) AS separation
FROM fmlist a JOIN contours b ON a.scs = b.scs LIMIT 20;
"""

