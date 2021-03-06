"""
This code takes in a downloaded class schedule from UCONN's Student Administration System,
and determines which classes are in what content area as defined in the Undergraduate Catalog.

It's easiest to select one term, one campus, and search for undergraduate level courses
only. This script does not list campuses or ways of instruction (In Person vs Hybrid, etc.)

This script does not have up to date values, and is meant as a method of quick checking, and not
actual verification. Double check the Undergraduate Catalog and the up-to-date listing on UCONN's
Student Administration System for availability and space.

Field  0: Class Number          - Individual classes                - 5 digits
Field  1: Subject Area          - What subject                      - 4 letters
Field  2: Catalog Number        - Corresponds to class catalog      - 4/5 alphanumeric
Field  3: Class Section         - Individual sections               - 3/4 alphanumeric
Field  4: Academic Career       - Undergraduate, graduate, etc.     - String
Field  5: Units                 - Amount of credits towards degree  - String, has =" "
Field  6: Campus                - What campus                       - 5 letters
Field  7: Session               - When class is held                - letters
Field  8: Description           - Description of class              - 30 characters
Field  9: Instruction Mode      - In Person/Hybrid/WWW/TV/etc.      - String
Field 10: Auto Enroll Sections  - Forced into these secutions       - 4 characters
Field 11: Enrollment Capacity   - Max amount in section             - Number
Field 12: Enrollment Current    - Current amount in section         - Number
Field 13: Specific Limitations  - Specific restrictions on enroll   - String
Field 14: Enrollment Slots Open - Amount of available slots left    - Number
Field 15: People on Wait List   - Amount on waitlist                - Number
Field 16: Instructor (Role)     - (PI), primary instructor, teacher - String
Field 17: Hours/Days/Location   - Time / Day / Location             - String
Field 18: Content Area          - Which content area class is       - 2 alphanumeric
"""

import argparse
from lxml.html import parse
from caList import *

def appendContentArea(c):
    """
    This function takes in one argument:
         c: class listings, as a list

    This takes the subject and catalog number per class listing
    and appends the content area to the class listing.
    """
    classes = c
    for r in range(1, len(classes)):
        key = classes[r][1] + ' ' + classes[r][2]
        if key in caDict:
            classes[r].append(caDict[key])
        else:
            classes[r].append('-')
    return classes

def formatFields(c):
    """
    This function takes in one argument:
        c: class listings, as a list

    This removes the =" and trailing " in the catalog number.
    For the units, the =" and trailing " are removed, as well
    as the additional .00; no observed classes are fractional units.
    """
    classes = c
    for row in classes[1:]:
        # row[2] = row[2][2:len(row[2]) - 1]
        if row[5] != None:
            row[5] = row[5].replace('.00', '')
            row[5] = row[5].replace('="', '')
            row[5] = row[5].replace('"', '')
            row[5] = row[5].replace(' ', '')
        row[16] = row[16].replace('\n\r', '')
    return classes

def printClasses(c, ca = 0, f = 0):
    """
    This function takes in three arguments:
             c: class listings, as a list
            ca: views classes based off of integer.
                0 = show all classes
                1 = show Arts and Humanities
                2 = show Social Sciences
                3 = show Science and Technology
                4 = show Diversity and Multiculturalism
                5 = show all classes with a content area
             f: views classes if they are full or not.
                0 = show all classes
                1 = show full classes only

    This prints out the classes in the class listing. If viewCA is True, it only prints
    out those classes found with a content area. By default, this will print out every
    content area. If ca is specified, then it will print out only those classes in a 
    a certain content area. If it is false, it prints out the class listing.
    """
    classes = c
    formattedString = '%(class)-5s %(subject)-4s %(catalog)-5s %(ca)-4s %(section)-7s %(units)-5s %(description)-30s %(autoenroll)-11s %(open)4s/%(enrolled)8s/%(max)3s/%(wait)4s %(instructor)-63s %(hours)s'

    print '%s %-10s %-4s %-7s %-5s %-30s %-11s %s %-63s %s' % ('Class', 'Course ID', 'CA', 'Section', 'Units', \
        'Description', 'Auto-Enroll', 'Open/Enrolled/Max/Wait', 'Instructor', 'Hours')
    
    for row in classes[1:]:
        # Map the data within the row to certain identifiers.
        mapping = {"class": row[0], "subject": row[1], "catalog": row[2], "ca": row[18], "section": row[3], 
                   "units": row[5], "description": row[8], "autoenroll": row[10], "open": row[14], "enrolled": row[12],
                   "max": row[11], "wait": row[15], "instructor": row[16], "hours": row[17]}
        # Show either only full classes or excluding full classes.
        if f != 0:
            # Show only full classes.
            if f == 1:
                if row[12] == row[11]:
                    if ca == 0:
                        print formattedString % mapping
                    else:
                        if not '-' in row[18]:
                            if ca == 5: 
                                print formattedString % mapping
                            else:
                                if str(ca) in row[18]:
                                    print formattedString % mapping
            # Exclude full classes.
            elif f == 2:
                # Thus only print out if open is greater than 0.
                if row[14] > '0':
                    if ca == 0:
                        print formattedString % mapping
                    else:
                        if not '-' in row[18]:
                            if ca == 5: 
                                print formattedString % mapping
                            else:
                                if str(ca) in row[18]:
                                    print formattedString % mapping
        # Show all classes, regardless.
        else:
            if ca == 0:
                print formattedString % mapping
            else:
                if not '-' in row[18]:
                    if ca == 5:
                        print formattedString % mapping
                    else:
                        if str(ca) in row[18]:
                            print formattedString % mapping

def validateArgs(a):
    """
    This function takes in one argument:
        a: arguments passed by the user

    This function determines if the values entered for:
        --show
        --full
    are valid. Raises an exception if not.
    """
    if not (0 <= a.show <= 5):
        raise Exception('Invalid number put in for show (0-5): ' + str(a.show))
    elif not (0 <= a.full <= 2):
        raise Exception('Invalid number put in for full (0-2): ' + str(a.full))

def main():
    parser = argparse.ArgumentParser(description = 'This script determines which classes are in what content areas based off of the Undergraduate Catalog of 2015-2016.')
    parser.add_argument('-c', '--classes', type = str, help = 'Classes file from the Student Administration service.', required = True)
    parser.add_argument('-s', '--show', type = int, default = 0, help = 'Content area number from the Undergraduate Catalog. 0 shows all classes, 1-4 shows specific content areas, 5 shows all classes with a content area.', required = False)
    parser.add_argument('-f', '--full', type = int, default = 0, help = 'Shows what classes are full. 0 shows all classes, 1 shows only full classes, 2 excludes full classes.', required = False)

    args = parser.parse_args()
    validateArgs(args)

    try:
        data = parse(args.classes)
        rows = data.xpath("body/table")[0].findall("tr")
        classes = list()
        for row in rows:
            classes.append([c.text for c in row.getchildren()])

        classes = formatFields(classes)
        classes = appendContentArea(classes)
        printClasses(classes, args.show, args.full)
    except IOError, Argument:
        print 'The file(s) entered cannot be accessed:', Argument

if __name__ == "__main__":
    main()