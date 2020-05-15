#!/usr/bin/python3

import sys
import subprocess
import re
import hashlib
import requests
import logging
from logging.handlers import TimedRotatingFileHandler

from xml.etree import ElementTree

logname = "/home/bbuser/logs/participants.log"
timedhandler = TimedRotatingFileHandler(logname, when='midnight', interval=1)
timedhandler.suffix = "%Y%m%d"

formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt="%H:%M")
timedhandler.setFormatter(formatter)

console_handler = logging.StreamHandler()
#console_handler.setLevel(logging.ERROR)

logger = logging.getLogger('report')
logger.addHandler(timedhandler)
logger.addHandler(console_handler)

logger.setLevel(logging.DEBUG)

###
## bbb-conf --secret
#
#    URL: https://.../bigbluebutton/
#    Secret: ....
#

verbose = False
if len(sys.argv) > 1 and sys.argv[1] == '-v':
    verbose = True

tmp = subprocess.run(['/usr/bin/bbb-conf', '--secret'], stdout=subprocess.PIPE, universal_newlines=True)
#PYTHON 3.7 tmp = subprocess.run(['/usr/bin/bbb-conf', '--secret'], capture_output=True, text=True)
output = tmp.stdout

URL = None
secret = None

for line in output.splitlines():
    m = re.search('URL: (?P<URL>.*/bigbluebutton/)', line)
    if m:
        URL = m.group('URL')
        continue
    m = re.search('Secret: (?P<secret>.*)$', line)
    if m:
        secret = m.group('secret')


if not URL or not secret:
    logger.error('error getting URL and/or secret. Is "bbb-conf --secret" returning it?')

APIURL=URL + 'api/'

apimethod='getMeetings'
querystring=''

h = hashlib.sha1((apimethod+querystring+secret).encode('utf-8'))
checksum = h.hexdigest()

if len(querystring) > 0:
    querystring = querystring + '&'

requesturl = APIURL + apimethod + '?' + querystring + 'checksum=' + checksum

response = requests.get(requesturl)
tree = ElementTree.fromstring(response.content)

if tree.find('returncode').text != 'SUCCESS':
    logger.error('error getting API data')
    sys.exit(1)
meetings = tree.find('meetings')

num_meetings = 0
num_users = 0
num_video = 0

for m in meetings.iter('meeting'):
    meetname = m.find('meetingName').text
    meetid = m.find('meetingID').text
    participants = m.find('participantCount').text
    video = m.find('videoCount').text

    meta = m.find('metadata')
    origin = meta.find('bbb-origin').text
    if meta.find('bbb-context') is not None:
        meetname = meta.find('bbb-context').text + ' / ' + meetname

    # logger.info('--[ %s ]---< %s / %s >---' % (meetname, meetid, origin))
    logger.info('--[ %s ]---' % (meetname))
    if verbose:
        'verbose is identical to normal yet'
    for a in m.find('attendees').iter('attendee'):
        v = ' '
        if a.find('hasVideo').text == 'true':
            v = 'V'
        audio = ' '
        if a.find('hasJoinedVoice').text == 'true':
            audio = 'A'
        logger.info('    +--[ %-10s ]--(%s%s)-> %s' % (a.find('role').text, v, audio, a.find('fullName').text))
    logger.info('    +==> %2s participants' % (participants,))
    logger.info('    +==> %2s videostreams' % (video,))

    num_meetings += 1
    num_users += int(participants)
    num_video += int(video)

#print('total: %2i meetings, %2i users, %2i videostreams' % (num_meetings, num_users, num_video))
logger.info('total: %2i meetings, %2i users, %2i videostreams' % (num_meetings, num_users, num_video))

