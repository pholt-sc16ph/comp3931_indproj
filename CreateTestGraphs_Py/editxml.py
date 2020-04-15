import os
import fileinput

def replace_in():
    pre, ext = os.path.splitext("Connectivity.xml")
    os.rename("Connectivity.xml", pre + ".txt")


    textToSearch = "in_"
    textToReplace = "in"
    fileToSearch  = "Connectivity.txt"

    tempFile = open(fileToSearch, 'r+')

    for line in fileinput.input(fileToSearch):
        tempFile.write(line.replace(textToSearch, textToReplace))
    tempFile.close()

    pre1, ext1 = os.path.splitext("Connectivity.txt")
    os.rename("Connectivity.txt", pre1 + ".xml")