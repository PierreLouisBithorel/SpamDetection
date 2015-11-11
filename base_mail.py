from urllib2 import urlopen
import tarfile
import os

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

# Archivage en local des données depuis un répertoir distant.
currentDir = os.getcwd()

if not os.path.exists(currentDir + "/bases/"):
    os.mkdir(currentDir + "/bases")
    downloadBases(currentDir)

# Création des bases de données.
