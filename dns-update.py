import httplib2
import json
import logging
import os

DYN_HOST_NAME = "mytestdomain.strangled.net"
DNS_REGISTRAR_API_URL = "https://sync.afraid.org/u/%s/?hostname=%s&myip=%s&content-type=json"

def create_dns_update_url(domain_api_key, ip_address):
    update_url = DNS_REGISTRAR_API_URL % (domain_api_key, DYN_HOST_NAME, ip_address) 
    logging.debug("Update URL: %s" % update_url)
    return update_url

def set_new_ip(domain_api_key, ip_address):
    dynamic_dns_update_url = create_dns_update_url(domain_api_key, ip_address)
    h = httplib2.Http(".cache")
    (resp_headers, content) = h.request(dynamic_dns_update_url, "GET")
    logging.debug("Response: %s", content)

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

def load_dns_api_key_from_environment():
    domain_api_key = os.getenv('FREE_DNS_TOKEN')
    if not domain_api_key:
        logging.error("Dynamic DNS token not set in environment!")
    else:
        logging.debug("Dynamic DNS token retrieved from environment")
    return domain_api_key

def create_logger():
    logging.basicConfig(filename='dns-updater.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

if __name__ == '__main__':
    create_logger()
    domain_api_key = load_dns_api_key_from_environment()
    ext_ip = retrieve_ip_address()
    set_new_ip(domain_api_key, ext_ip)
    logging.info("External IP Address is %s" % ext_ip)