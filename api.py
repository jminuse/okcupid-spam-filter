import re, time, random, sys
import requests

def get_string_between(string,a,b):
	start = string.find(a)
	string = get_thread.content[start:get_thread.content.find(b, start)]
	return string

def delete_thread(session, content):
	form = get_string_between(content, 'id="delete_button"', '</form>')
	hidden_values = re.findall('type="hidden" name="([^"]+)" (?:id="[^"]+" )?value="([^"]+)"', form)
	form_data = {'deletethread':'DELETE'}
	for h in hidden_values:
		form_data[ h[0] ] = h[1]
	delete_response = session.post('http://www.okcupid.com/mailbox', data=form_data, params=thread_data)

def login(username, password):
	session = requests.Session()
	credentials = {'username': username, 'password': password, 'dest': '/home'}
	login_response = session.post('https://www.okcupid.com/login', data=credentials)
	return session

def score_message(message_original):
	bad_strings = ['oriental', 'exotic']
	good_strings = []
	message = message_original.lower()
	score = 0
	for string in bad_strings:
		if string in message: score -= 10
	for string in good_strings:
		if string in message: score += 10
	return score

username = 'fill this in'
password = 'fill this in too'
if username == 'fill this in':
	print 'Fill in your username and password!'
	sys.exit(1)
session = login(username, password)

time.sleep(1+random.random())
messages_response = session.get('http://www.okcupid.com/messages')
thread_ids = re.findall('threadid="([^"]+)"', messages_response.content)

for thread in thread_ids:
	thread_data = {'readmsg': 'true', 'threadid': thread, 'folder': 1}
	time.sleep(1+random.random())
	get_thread = session.get('http://www.okcupid.com/messages', params=thread_data)
	message = get_string_between(get_thread.content, '<div class="message_body">', '</div>')

	if score_message(message) < 0:
		print 'Deleting "%s"' % message
		time.sleep(1+random.random())
		delete_thread(session, get_thread.content)

