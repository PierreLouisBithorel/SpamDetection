from urllib2 import urlopen
import tarfile
import os
import pandas

def downloadBases(currentDir):
    """
    Téléchargement des bases de données au format .tar.bz2 et extraction.
    """
    
    depot = "http://spamassassin.apache.org/publiccorpus/"
    bases = ["20021010_easy_ham.tar.bz2", "20021010_hard_ham.tar.bz2", "20021010_spam.tar.bz2"]

    for i in bases:
        baseName = i.split('_',1)[1].split('.',1)[0]
        remoteFile = urlopen(depot + i)
        localFile = open(currentDir + "/bases/" + i, 'wb')
        localFile.write(remoteFile.read())
        localFile.close()
        remoteFile.close()
        tarDir = tarfile.open(currentDir + "/bases/" + i)
        tarDir.extractall(currentDir + "/bases/")
        tarDir.close()
        os.remove(currentDir + "/bases/" + i)

    return

class mail:
    """
    Mail analysis for the construction of a structured data set.
    """
    
    def _init_(self, type, id):
        self.type = type
        self.number = None
        self.date = None
        self.id = id
        self.body = None
        self.subject = None
        self.contextType = None

    def importation(type, number):
        localfile = open(currentDir + "/bases/" + type + number, 'r')
        

# Data storing from a distant repositorie.
currentDir = os.getcwd()

if not os.path.exists(currentDir + "/bases/"):
    os.mkdir(currentDir + "/bases")
    downloadBases(currentDir)

# Creation of a structured data set.
architecture = {type : os.listdir(currentDir + "/bases/" + type) for type in os.listdir(currentDir + "/bases")}

for type in architecture:
    for number in architecture[type]:
        
