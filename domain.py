import whois
from datetime import datetime

class Domain(whois.Domain):

    @property
    def expiration_days(self):
        return "AVAILABLE" if self.expiration_date is None else (self.expiration_date - datetime.now()).days
