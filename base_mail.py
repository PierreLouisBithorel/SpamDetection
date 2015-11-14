from urllib2 import urlopen
from email import message_from_file
import tarfile, os, pandas, re

def downloadBases(currentDir):
    """ Download and extract datas in format .tar.bz2. """
    depot = "http://spamassassin.apache.org/publiccorpus/"
    bases = ["20021010_easy_ham.tar.bz2", "20021010_hard_ham.tar.bz2", "20021010_spam.tar.bz2"]
    for i in bases:
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

class email:
    """ Mail analysis and dataset construction. """

    def __init__(self, adress):
        emailMessage = message_from_file(open(adress, 'r'))
        self.MessageID = emailMessage.get('Message-ID')
        self.From = emailMessage.get('From')
        self.Subject = emailMessage.get('Subject')
        self.Date = emailMessage.get('Date')
        self.Cc = self.removeSepInString(emailMessage.get('Cc'))
        self.Encoding = emailMessage.get('Content-Transfer-Encoding')
        self.Type = [emailMessage.get_content_maintype(), emailMessage.get_content_subtype()]
        self.AttachedFile = emailMessage.get_filename()
        self.IsMultipart = emailMessage.is_multipart()
        self.Body = emailMessage.get_payload()

    def removeSepInString(self, string):
        """ Remove separators in an email list. """
        print(string)
        if string != None and string != '':
            print('\n')
            test = { }
            print(string.split(','))
            for email in string.split(','):
                key = re.sub('[)"\']$', '', re.sub('^[\n\t\'(" ]*', '', re.sub('[ \n\t]*[<]?[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[>]?', '', email)))
                value = re.sub('>', '', re.sub('<', '', re.search('[<]?[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[>]?', email).group(0)))
                               # .split('<')[1].split('>')[0]
                if key == '': key = None
                print(key)
                print(value)
                test[value] = key
        else:
            test = None
        print(test)
        return test


# Data storing from a distant repositorie.
currentDir = os.getcwd()

if not os.path.exists(currentDir + "/bases/"):
    os.mkdir(currentDir + "/bases")
    downloadBases(currentDir)

# Creation of a structured data set.
architecture = {type : os.listdir(currentDir + "/bases/" + type) for type in os.listdir(currentDir + "/bases")}
error = [ ]

df = pandas.DataFrame(columns = ['Message-ID', 'Type', 'From', 'Subject', 'Date', 'Forme', 'AttachedFile', 'MultiPart', 'Body'])
row = 1

i=1
for type in architecture:
    for file in architecture[type]:
        email(currentDir + "/bases/" + type + "/" + file)
        i+=1
        print(i)
        
# df.to_csv(currentDir + "/bases/base.txt", sep="\t", index=False)



# emailMessage = message_from_file(open("/home/pierre-antoine/Documents/Cours/Python/SpamDetection/bases/spam/0064.d700742b9815d990b2e5a7921e8d854c",'r'))
