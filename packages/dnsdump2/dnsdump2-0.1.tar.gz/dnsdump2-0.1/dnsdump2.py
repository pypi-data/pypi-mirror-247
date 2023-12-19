import json
import requests
from bs4 import BeautifulSoup
from collections.abc import MutableMapping

class DnsDumpster:
    def __init__(self):
        self.headers = {"Referer": "https://dnsdumpster.com"}
        r = requests.get("https://dnsdumpster.com", headers=self.headers)
        doc = BeautifulSoup(r.text.strip(), "html.parser")
        try:
            tag = doc.find("input", {"name": "csrfmiddlewaretoken"})
            self.csrftoken = tag['value']
            self.headers = {
                "Referer": "https://dnsdumpster.com",
                "Cookie": f"csrftoken={self.csrftoken};"
            }
        except:
            pass

    def _clean_table(self, table, record_type=0):
        retval = {}
        if record_type == 1:
            for idx, tag in enumerate(table.find_all('td')):
                retval[idx] = tag.string
        for idx, tag in enumerate(table.find_all('td', {'class': 'col-md-4'})):
            clean_name = tag.text.replace('\n', '')
            clean_ip = tag.a['href'].replace('https://api.hackertarget.com/reverseiplookup/?q=', '')
            retval[idx] = {'ip': clean_ip, 'host': clean_name}
        return retval

    def dump(self, target):
        retval = {}
        data = {"csrfmiddlewaretoken": self.csrftoken, "targetip": target}
        r = requests.post("https://dnsdumpster.com", headers=self.headers, data=data)
        doc = BeautifulSoup(r.text.strip(), "html.parser")
        tables = doc.find_all('table')
        try:
            retval['dns'] = self._clean_table(tables[0])
            retval['mx'] = self._clean_table(tables[1])
            retval['txt'] = self._clean_table(tables[2], 1)
            retval['host'] = self._clean_table(tables[3])
            return retval
        except:
            return False

    def hostsearch(self, target):
        try:
            r = requests.get(f"https://api.hackertarget.com/hostsearch/?q={target}")
            return r.text
        except:
            return "An error occurred."

    def reversedns(self, target):
        try:
            r = requests.get(f"https://api.hackertarget.com/reversedns/?q={target}")
            return r.text
        except:
            return "An error occurred."

    def dnslookup(self, target):
        try:
            r = requests.get(f"https://api.hackertarget.com/dnslookup/?q={target}")
            return r.text
        except:
            return "An error occurred."

    def pagelinks(self, target):
        try:
            r = requests.get(f"https://api.hackertarget.com/pagelinks/?q={target}")
            return r.text
        except:
            return "An error occurred."

    def httpheaders(self, target):
        try:
            r = requests.get(f"https://api.hackertarget.com/httpheaders/?q={target}")
            return r.text
        except:
            return "An error occurred."


print("""


██████╗  █████╗ ██╗   ██╗██████╗ ██╗   ██╗███╗   ███╗
██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗██║   ██║████╗ ████║
██████╔╝███████║ ╚████╔╝ ██████╔╝██║   ██║██╔████╔██║
██╔══██╗██╔══██║  ╚██╔╝  ██╔══██╗██║   ██║██║╚██╔╝██║
██████╔╝██║  ██║   ██║   ██║  ██║╚██████╔╝██║ ╚═╝ ██║
╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝
                                                     

    """)

target = input("Enter the target domain: ")

# Create an instance of DnsDumpster
dnsdump = DnsDumpster()

# Perform various actions based on user prompts
action = input("Select action (1: Host Search, 2: Reverse DNS, 3: DNS Lookup, 4: DNS Dump, 5: Page Links, 6: HTTP Headers, 7: All): ")

output_to_file = input("Do you want to save the output to a text file? (y/n): ").lower() == 'y'

output_data = None  # Variable to store output data

if action == '1':
    output_data = dnsdump.hostsearch(target)
elif action == '2':
    output_data = dnsdump.reversedns(target)
elif action == '3':
    output_data = dnsdump.dnslookup(target)
elif action == '4':
    output_data = json.dumps(dnsdump.dump(target), indent=1)
elif action == '5':
    output_data = dnsdump.pagelinks(target)
elif action == '6':
    output_data = dnsdump.httpheaders(target)
elif action == '7':
    output_data = {
        'dns': dnsdump.dump(target),
        'hostsearch': dnsdump.hostsearch(target),
        'reversedns': dnsdump.reversedns(target),
        'dnslookup': dnsdump.dnslookup(target),
        'pagelinks': dnsdump.pagelinks(target),
        'httpheaders': dnsdump.httpheaders(target)
    }
    output_data = json.dumps(output_data, indent=1)

# Print or save the output based on user choice
if output_to_file:
    with open("results.txt", "w") as file:
        file.write(str(output_data))
    print(f"Output saved to 'results.txt' in the same directory.")
else:
    print(output_data)
