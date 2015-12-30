# UCONN Content Areas
Takes in class listings from the Student Administration service, outputs which classes are in what content area.
This is intended for Undergraduate classes only.

**Usage**: classes.py -c **classes** -s **show** -f **full**

* **classes** is the ps.xls file downloaded from the Student Administration service

* **show** defines what classes will be shown. 0 shows all classes, regardless if they are in a content area or not. 1-4 shows classes specific to those content areas. 5 shows classes that belong to any content area.

* **full** defines if all the classes will be shown, or only full classes. 0 shows all classes, 1 shows only full classes.