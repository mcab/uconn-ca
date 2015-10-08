"""
2015-10-08: v0.1, initial release.

This code takes in a downloaded class schedule from UCONN's Student Administration System,
and determines which classes are in what content area as defined in the Undergraduate Catalog.

It's easiest to select one term, one campus, and search for undergraduate level courses
only. This script does not list campuses or ways of instruction (In Person vs Hybrid, etc.)

This script does not have up to date values, and is meant as a method of quick checking, and not
actual verification. Double check the Undergraduate Catalog and the up-to-date listing on UCONN's
Student Administration System for availability and space.

Field  0: Class Number          - 5 digits
Field  1: Subject Area          - 4 letters
Field  2: Catalog Number        - 5 characters, excluding =" "
Field  3: Class Section         - 4 characters
Field  4: Academic Career       - Undergraduate, typically.
Field  5: Campus                - 5 letters
Field  6: Session               - Regular?
Field  7: Description           - 30 characters
Field  8: Instruction Mode      - In Person/Hybrid/WWW/TV/etc.
Field  9: Auto Enroll Sections  - 4 characters
Field 10: Enrollment Capacity   - number
Field 11: Enrollment Current    - number
Field 12: Specific Limitations  - text information
Field 13: Enrollment Slots Open - number
Field 14: People on Wait List   - number
Field 15: Instructor (Role)     - letters
Field 16: Hours/Days/Location   - multiple times and days
Field 17: Content Area          - up to two characters

"""

import argparse
from lxml.html import parse

def appendContentArea(c, ca):
    """
    This function takes in two arguments:
         c: class listings, as a list
        ca: content areas, as a list

    This takes the subject and catalog number per class listing,
    and searches for it by every row in the content areas listing.

    There is possible mischecking based off of this method due to checking
    only the first four characters and not if it is a Q/W course.
    """
    classes = c
    contentArea = ca
    for r in range(1, len(classes)):
        subject = classes[r][1]
        catalogNumber = classes[r][2]
        contentAreaFound = False
        for i in range(0, len(contentArea)):
            if subject in contentArea[i][1] and catalogNumber[0:4] in contentArea[i][1]:
                classes[r].append(contentArea[i][0])
                contentAreaFound = True
                break
        if contentAreaFound == False:
            classes[r].append('N/A')
    return classes

def formatCatalogNumber(c):
    """
    This function takes in one argument:
        c: class listings, as a list

    This removes the =" and trailing " in the catalog number
    in the original .xls file for classes.
    """
    classes = c
    for row in classes[1:]:
        row[2] = row[2][2:len(row[2]) - 1]
    return classes

def printClasses(c, viewCA=True):
    """
    This function takes in two arguments:
             c: class listings, as a list
        viewCA: (default true) view only content area courses, as a boolean

    This prints out the classes in the class listing. If viewCA is True,
    it only prints out those classes found with a content area. If it is
    false, it prints out the class listing.
    """
    classes = c
    print '%s %s %s %-4s %s %-30s %-11s %s %-76s %s' % ('Class', 'Subj', 'Catalog', 'CA', 'Section', 'Description', \
        'Auto-Enroll', 'Open/Enrolled/Max/Wait', 'Instructor', 'Hours')
    if viewCA == True:
        for row in classes[1:]:
            if not 'N/A' in row[17]:
                print '%-5s %-4s %-7s %-4s %-7s %-30s %-11s %4s/%8s/%3s/%4s %-76s %s' % (row[0], row[1], row[2], \
                    row[17], row[3], row[7], row[9], row[13], row[11], row[10], row[14], row[15].replace('\n', ''), row[16])
    else:
        for row in classes[1:]:
            print '%-5s %-4s %-7s %-4s %-7s %-30s %-11s %4s/%8s/%3s/%4s %-76s %s' % (row[0], row[1], row[2], \
                row[17], row[3], row[7], row[9], row[13], row[11], row[10], row[14], row[15].replace('\n', ''), row[16])

def processContentArea(ca, d):
    """
    This function takes in two arguments:
        ca: content areas, as a list
         d: delimiter, as a string

    This function splits up the content area listings by whatever
    delimiter is used, stores it as a list, and returns the list.
    """
    f = open(ca, 'r')
    data = list()
    for line in f.readlines():
        data.append(line.split(d));
    return data

def main():
    parser = argparse.ArgumentParser(description = 'This script determines which classes are in what content areas based off of the Undergraduate Catalog of 2015-2016.')
    parser.add_argument('-c', '--classes', help = 'Classes file from the Student Administration service', required = True)
    parser.add_argument('-ca', '--contentarea', help = 'Content area file from the Undergraduate Catalog', required = True)
    args = parser.parse_args()

    data = parse(args.classes)
    rows = data.xpath("body/table")[0].findall("tr")
    classes = list()
    for row in rows:
        classes.append([c.text for c in row.getchildren()])

    classes = formatCatalogNumber(classes)
    contentAreas = processContentArea(args.contentarea, ' ^ ')
    classes = appendContentArea(classes, contentAreas)
    printClasses(classes, True)

if __name__ == "__main__":
    main()