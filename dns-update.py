import httplib2
import json
import logging

DYN_HOST_NAME = "mobile"
DOMAIN_NAME = "bit-shift.net"
DNS_REGISTRAR_API_URL = "https://api.dev.name.com/"
DNS_DOMAIN_CREATE_URL = "api/dns/create/"

def create_dns_update_payload(ip_address):
    create_json = {
        "hostname" : DYN_HOST_NAME,
        "type" : "A",
        "content" : ext_ip,
        "ttl" : 86400,
        "priority" : 10
    }

    return create_json

def set_new_ip(ip_address):
    create_domain_json = create_dns_update_payload(ip_address)
    h = httplib2.Http(".cache")
    create_domain_URL = "%s%s" % DNS_REGISTRAR_API_URL, DNS_DOMAIN_CREATE_URL
    (resp_headers, content) = h.request(create_domain_URL, "POST", body=create_domain_json, headers={})

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
    set_new_ip(ext_ip)
    logging.info("External IP Address is %s" % ext_ip)