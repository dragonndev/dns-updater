import json
import logging
import time
import os
from pathlib import Path
import httplib2 #https://github.com/httplib2/httplib2
import schedule #https://github.com/dbader/schedule

class DNSUpdater(object):

    """Class to update IP address information for a dynamic DNS hosting service"""
    
    dns_registration_api_url = "https://sync.afraid.org/u/%s/?myip=%s&content-type=json"

    def __init__(self):
        self.create_logger()
        self.app_config = self.load_configuration_from_file()
        self.dns_api_token = self.load_dns_api_token()
        self.dns_hostname = self.load_dns_hostname()
        self.schedule_dns_update()

    def schedule_dns_update(self):
        schedule.every(1).days.do(self.update_dyn_dns_setting)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def update_dyn_dns_setting(self):
        ext_ip = self.retrieve_ip_address()
        self.set_new_ip(ext_ip)
        logging.info("External IP Address is %s", ext_ip)

    def create_dns_update_url(self, ip_address):
        update_url = self.dns_registration_api_url % (self.dns_api_token, ip_address)
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

        content_str = content.decode('utf-8')

        resp_json = json.loads(content_str)
        return resp_json["ip"]

    def load_dns_hostname(self):
        dns_hostname = self.app_config["dns_hostname"]
        if dns_hostname is None:
            logging.error("Cannot load DNS hostname from configuration file.")
            raise AttributeError("Cannot load DNS hostname.")
        logging.debug("DNS name: {}, loaded from configuration file.".format(dns_hostname))
        
        return dns_hostname
    
    def load_dns_api_token(self):
        dns_api_token = os.getenv("FREE_DNS_API_TOKEN")
        if dns_api_token is None:
            logging.error("DNS API token not set in environment.")
            raise AttributeError("Cannot load DNS API token.")
        logging.debug("Dynamic DNS API token loaded from environment")
        
        return dns_api_token
        
    def load_configuration_from_file(self):
        my_file = Path("./config.json")
        if not my_file.is_file():
            raise FileNotFoundError("Configuration file, config.json, not found.")
        with open('config.json', 'r', encoding='utf-8-sig') as json_file:
            text = json_file.read()
            app_config = json.loads(text)
            logging.info("Successfully loaded the configuration file. Host: {}".format(app_config["dns_hostname"]))
            return app_config
    	
    def create_logger(self):
        logging.basicConfig(filename='dns-updater.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s')

DNS_UPDATE = DNSUpdater()
