import json
import logging
import os
import httplib2 #https://github.com/httplib2/httplib2

class DNSUpdater(object):

    '''Class to update IP address information for a dynamic DNS hosting service'''
    
    dyn_host_name = "mytestdomain.strangled.net"
    dns_registration_api_url = "https://sync.afraid.org/u/%s/?myip=%s&content-type=json"

    def __init__(self):
        self.create_logger()
        self.domain_api_key = self.load_dns_api_key_from_environment()

    def update_dyn_dns_setting(self):
        ext_ip = self.retrieve_ip_address()
        self.set_new_ip(ext_ip)
        logging.info("External IP Address is %s", ext_ip)

    def create_dns_update_url(self, ip_address):
        update_url = self.dns_registration_api_url % (self.domain_api_key, ip_address)
        logging.debug("Update URL: %s", update_url)
        return update_url

    def set_new_ip(self, ip_address):
        dynamic_dns_update_url = self.create_dns_update_url(ip_address)
        h_client = httplib2.Http(".cache")
        (resp_headers, content) = h_client.request(dynamic_dns_update_url, "GET")
        logging.debug("Response headers: %s ", resp_headers)
        logging.debug("Response: %s", content)

    def retrieve_ip_address(self):
        h_client = httplib2.Http(".cache")
        (resp_headers, content) = h_client.request("https://api.ipify.org?format=json", "GET")
        logging.debug("Response Headers: %s", resp_headers)
        logging.debug("Response JSON: %s", content)
        if isinstance(content, bytes):
            logging.debug("Type is Bytes")

        content_str = content.decode('utf-8')

        resp_json = json.loads(content_str)
        return resp_json["ip"]

    def load_dns_api_key_from_environment(self):
        domain_api_key = os.getenv('FREE_DNS_TOKEN')
        if not domain_api_key:
            logging.error("Dynamic DNS token not set in environment!")
        else:
            logging.debug("Dynamic DNS token retrieved from environment")
        return domain_api_key

    def create_logger(self):
        logging.basicConfig(filename='dns-updater.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

DNS_UPDATE = DNSUpdater()
DNS_UPDATE.update_dyn_dns_setting()
#PrintOut DNS settings for sub-domain to validate IP address has been updated
