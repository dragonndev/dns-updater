import httplib2
import json
import logging

def retrieve_ip_address():
    h = httplib2.Http(".cache")
    (resp_headers, content) = h.request("https://api.ipify.org?format=json", "GET")
    logging.debug("Response Headers: %s" % resp_headers)
    logging.debug("Response JSON: %s" % content)
    if type(content) is bytes:
        logging.debug("Type is Bytes")

    content_str = content.decode('utf-8')

    resp_json = json.loads(content_str)
    return resp_json["ip"]

def create_logger():
    logging.basicConfig(filename='dns-updater.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

if __name__ == '__main__':
    create_logger()
    ext_ip = retrieve_ip_address()
    logging.info("External IP Address is %s" % ext_ip)