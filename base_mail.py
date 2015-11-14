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
error = [ ]

df = pandas.DataFrame(columns = ['Message-ID', 'From', 'Subject', 'Date', 'Type', 'AttachedFile', 'Body'])
row = 1

for type in architecture:
    for file in architecture[type]:
        emailMessage = message_from_file(open(currentDir + "/bases/" + type + "/" + file, 'r'))
        try:
            df.loc[row] = [emailMessage.get('Message-ID'), emailMessage.get('From'), emailMessage.get('Subject'), emailMessage.get('Date'), emailMessage.get_content_type().split('/',1)[0], emailMessage.get_filename(), emailMessage.get_payload().split()]
        except:
            error.append(currentDir + "/bases/" + type + "/" + file)
        row += 1

print(len(error))

# df.to_csv(currentDir + "/bases/base.txt", sep="\t", index=False)
# print(emailMessage.keys()) # Return all items in the header
