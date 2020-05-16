#!/usr/bin/env python
# DNS checker

from tqdm import tqdm
import whois
import argparse
import sys
from domain import Domain

def print_whois_results(available_domains, taken_domains):
    """
       Pretty print the whois results
    """
    if len(available_domains) > 0:
        print("\nAvailable domains:")
    else:
        print("\nAll the domains have been taken!")
    
    for available_domain in available_domains:
        print("  > %s" % available_domain)
    
    if len(taken_domains) > 0:
        print("\nTaken domains:")
        print("%-25s  %-35s  %-25s  %-4s" % ("DOMAIN NAME", "REGISTRAR", "EXPIRATION DATE", "DAYS LEFT"))

    for taken_domain in taken_domains:
        print("%-25s  %-35s  %-25s  %-s" % (
            taken_domain.name, 
            (taken_domain.registrar[:30] + '...') if len(taken_domain.registrar) > 30 else taken_domain.registrar, 
            taken_domain.expiration_date, 
            taken_domain.expiration_days
        ))

def is_blank_or_comment(s):
    """ function to check if a line
         starts with some character.
         Here # for comment or blank
    """
    # return true if a line starts with #
    return not s.strip() or s.startswith('#')

def bulk_whois(domains):
    """
       Execute domains name whois
    """
    available_domains = []
    taken_domains = []
    domains = tqdm(domains, unit="domain", ncols=100)
    for domain in domains:
        domains.set_description(domain)
        try:
            whois_data = whois.query(domain)
        except Exception as e:
            pass

        if whois_data is not None:
            whois_data.__class__ = Domain
            taken_domains.append(whois_data)
        else:
            available_domains.append(domain)

    return (available_domains, taken_domains)

def parse_cli_args():
    """
        Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(description='DNS Checker')
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help="File path containing the domains list")
    group.add_argument('-d', '--domain', help="Domain name")

    return parser.parse_args()
    
def main():
    args = parse_cli_args()
    print("")

    domains = []
    if args.file:
        with open(args.file, "r") as lines:
            for line in lines:
                line = line.rstrip()
                if is_blank_or_comment(line):
                    continue
                domains.append(line)
    elif args.domain:
        domains.append(args.domain)
    
    (available_domains, taken_domains) = bulk_whois(domains)
    taken_domains.sort(key=lambda domain: domain.expiration_days, reverse=False) 
    print_whois_results(available_domains, taken_domains)
        
if __name__ == "__main__":
    main()  
