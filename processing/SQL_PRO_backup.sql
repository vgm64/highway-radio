
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

# Attempt to map each contour to category
SELECT fcc.id, fmlist.id, fcc.callsign, fmlist.program, fcc.scs fccscs, fmlist.scs fmlistscs, fmlist.cat
FROM contours fcc 
JOIN 
  (SELECT * FROM fmlist WHERE program LIKE 'KG%' ) fmlist
ON fcc.scs = fmlist.scs
WHERE fcc.callsign LIKE "KG%"
GROUP BY fcc.id
LIMIT 1000;

SELECT cat, COUNT(cat) FROM fmlist GROUP BY cat;

# List contours for KGMZ
SELECT fcc.id, fcc.callsign, fcc.scs
FROM contours fcc 
WHERE fcc.callsign LIKE "KGMZ%"
LIMIT 1000;

# List fmlist entries for KGMZ
SELECT fmlist.id, fmlist.program, fmlist.scs, fmlist.cat, fmlist.reg, fmlist.frequency
FROM fmlist
WHERE fmlist.program LIKE "KG%";

# For each contour, query fmlist for that scs and count the different types of cats.
SELECT fcc.id, fcc.callsign, fcc.scs
