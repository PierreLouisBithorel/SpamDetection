from urllib2 import urlopen
import tarfile
import os
import pandas
from email import message_from_file

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

# Data storing from a distant repositorie.
currentDir = os.getcwd()

if not os.path.exists(currentDir + "/bases/"):
    os.mkdir(currentDir + "/bases")
    downloadBases(currentDir)

# Creation of a structured data set.
architecture = {type : os.listdir(currentDir + "/bases/" + type) for type in os.listdir(currentDir + "/bases")}

for type in architecture:
    for file in architecture[type]:
        emailMessage = message_from_file(open(currentDir + "/bases/" + type + "/" + file, 'r'))
        emailMessage.get('From')
        

emailMessage = message_from_file(open(currentDir + "/bases/spam/" + architecture['spam'][0]))
print(emailMessage.get('From'))
