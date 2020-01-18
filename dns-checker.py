#!/usr/bin/env python
# DNS checker

import whois
import argparse
import sys
from domain import Domain

def print_heading():
    """
       Pretty print heading
    """
    print("%-25s  %-35s  %-25s  %-4s" % ("DOMAIN NAME", "REGISTRAR", "EXPIRATION DATE", "DAYS LEFT"))

def print_whois(whois_data):
    """
       Pretty print the domain information
    """
    
    print("%-25s  %-35s  %-25s  %-s" % (
        whois_data.name, 
        (whois_data.registrar[:30] + '...') if len(whois_data.registrar) > 30 else whois_data.registrar, 
        whois_data.expiration_date, 
        whois_data.expiration_days
    ))

def is_blank_or_comment(s):
    """ function to check if a line
         starts with some character.
         Here # for comment or blank
    """
    # return true if a line starts with #
    return not s.strip() or s.startswith('#')

def execute_whois(domain_name):
    """
       Execute domain name whois
    """
    try:
        whois_data = whois.query(domain_name)
    except Exception as e:
        print("Failed to whois the domain name '%s'. Exception %s" % (domain_name, e))
        sys.exit(1)

    if whois_data is not None:
        whois_data.__class__ = Domain
    else:
        whois_data = Domain(domain_name)

    return whois_data

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

    print_heading()

    if args.file:
        with open(args.file, "r") as lines:
            for line in lines:
                if is_blank_or_comment(line):
                    continue
                domain_name = line
                whois_data = execute_whois(domain_name)
                print_whois(whois_data)
    elif args.domain:
        whois_data = execute_whois(args.domain)
        print_whois(whois_data)
        
if __name__ == "__main__":
    main()  