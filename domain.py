import whois
from datetime import datetime

class Domain(whois.Domain):

    def __init__(self, domain_name):
        super(Domain, self).__init__({"domain_name": [domain_name], "registrar": ["None"], "creation_date": [""], "expiration_date": [""], "updated_date": [""], "name_servers": [""]})

    @property
    def expiration_days(self):
        return "AVAILABLE" if self.expiration_date is None else (self.expiration_date - datetime.now()).days
