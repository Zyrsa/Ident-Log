import urllib.request, gspread, os, time
from oauth2client.service_account import ServiceAccountCredentials

if os.path.isfile("ident.txt"):
	identfile = open("ident.txt", "r")
	identfile.seek(0)
	old_ident = identfile.readline()
	identfile.close()
else:
	old_ident = False

ident = urllib.request.urlopen('https://niho.net/ident/').read().decode('utf8')

old_ident = str(old_ident)
ident = str(ident)

if ident != old_ident:
	identfile = open("ident.txt", "w")
	identfile.write("%s" % ident)
	identfile.close()

	scope = [
	    'https://spreadsheets.google.com/feeds',
	    'https://www.googleapis.com/auth/drive'
	]
	creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
	client = gspread.authorize(creds)

	sheet = client.open('identlog').sheet1

	date = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
	time = str(time.strftime('%H:%M', time.localtime(time.time())))
	row = [date, time, ident]
	index = 1

	sheet.insert_row(row, index)
	print("Ip added to log.")
else:
	print("Nothing to update.")
