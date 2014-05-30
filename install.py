import os
import glob

path =os.path.dirname(os.path.abspath(__file__))
print ('Ensure all the companies of interest are in the "companies.txt". \nAll files in data will be deleted.')
input('press any key')

# check id there is a data folder, if not it makes one
if not 'data' in glob.glob('*'):
    os.mkdir('data')


# deletes all previous data
toDelete = glob.glob('data/*')
for f in toDelete:
    os.remove(f)

# makes new empty stock files
f=open('companies.txt','r')
companies = f.read().split('\n')
header = companies[0]
companies = companies[1:]
f.close()
for f in companies:
    F = open('data/'+f+'.csv','w')
    F.write(header+'\n')
    F.close()


print('ready to start, use history maker to track stocks.')
