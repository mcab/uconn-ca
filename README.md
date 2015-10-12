# UCONN Content Areas
Takes in class listings from the Student Administration service, outputs which classes are in what content area.

**Usage**: classes.py -c **CLASSES** -ca **CONTENTAREA** -s **SHOW**

* **CLASSES** is the ps.xls file downloaded from the Student Administration service

* **CONTENTAREA** is the contentarea file in the repository, or a delimited list of courses based off of the information given in the undergraduate catalog.

* **SHOW** defines what classes will be shown. 0 shows all classes, regardless if they are in a content area or not. 1-4 shows classes specific to those content areas. 5 shows classes that belong to any content area.