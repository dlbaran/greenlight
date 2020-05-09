import requests as req
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger('report')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('report.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)


print 'running rooms: '

res = req.get("https://meet.kntu.ac.ir/bigbluebutton/api/getMeetings?checksum=aca79e66c07bc444f1f6a2db4429408b5cc131ec")
print res.content
root = ET.fromstring(res.content)

count = 0
num_meeting = 0
for meet in root.iter('meeting'):
    num_meeting += 1
    for attendees in meet.iter('attendees'):
        print len(attendees)
        count += len(attendees)



print 'number of online meetings: ' + str(num_meeting)
print 'all attendeess in room: '+ str(count)

logger.info('number of online meetings: ' + str(num_meeting))
logger.info('all attendeess in room: ' + str(count))

# https://meet.kntu.ac.ir/bigbluebutton/api/getMeetings?checksum=aca79e66c07bc444f1f6a2db4429408b5cc131ec
