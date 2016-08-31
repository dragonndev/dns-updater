import httplib2
import json

h = httplib2.Http(".cache")
(resp_headers, content) = h.request("https://api.ipify.org?format=json", "GET")
print ("Response Headers: ", resp_headers)
print ("Response JSON: ", content)
if type(content) is bytes:
    print ("Type is Bytes")

content_str = content.decode('utf-8')

resp_json = json.loads(content_str)
print ("IP Address: %s" % resp_json["ip"])