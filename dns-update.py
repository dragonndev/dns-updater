import httplib2

h = httplib2.Http(".cache")
(resp_headers, content) = h.request("https://api.ipify.org?format=json", "GET")
print ("Response Headers: ", resp_headers)
print ("Response JSON: ", content)