# Create the table used to map contours to fmlist entries for categories.
CREATE TABLE `contour_cat_map` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `contour_id` int(11) DEFAULT NULL,
  `fmlist_id` int(11) DEFAULT NULL,
  `cat` char(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

# Insert into a new contour_cat_map table the contour-map relation
INSERT INTO contour_cat_map (contour_id, fmlist_id, cat)
  (SELECT fcc.id, fmlist.id, fmlist.cat
  FROM contours fcc 
  JOIN 
      (SELECT * FROM fmlist) fmlist
  ON fcc.scs = fmlist.scs
  GROUP BY fcc.id
);
