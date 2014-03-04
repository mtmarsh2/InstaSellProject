from nexmomessage import NexmoMessage
API_KEY = '67ac5f35'
API_SECRET = '420b4115'
DESTINATION_NUMBER = '16302071793'

YOUR_NUMBER = '14844409627'
msg = {
	'reqtype':'json',
	'api_key':API_KEY,
	'api_secret':API_SECRET,
	'from':YOUR_NUMBER,
	'to':DESTINATION_NUMBER,
	'text':'marshall'
	}

sms = NexmoMessage(msg)
sms.set_text_info(msg['text'])
res = sms.send_request()
if res:
	print res
	print 'response'
else:
	print res
