#!/usr/bin/env python
# DNS checker

import whois
import argparse
import sys
from datetime import datetime

def print_heading():
    """
       Pretty print heading
    """
    print("%-25s  %-35s  %-30s  %-4s" % ("DOMAIN NAME", "REGISTRAR", "EXPIRATION DATE", "DAYS LEFT"))

def print_whois(whois_data):
    """
       Pretty print the domain information
    """
    print("%-25s  %-35s  %-30s  %-d" % (whois_data["name"], whois_data["registrar"], whois_data["expiration_date"], whois_data["days_remaining"]))

def execute_whois(domain_name):
    """
       Execute domain name whois
    """
    try:
        whois_data = whois.query(domain_name)
    except Exception as e:
        print("Failed to whois the domain name '%s'. Exception %s" % (domain_name, e))
        sys.exit(1)

    try:
        expiration_days = (whois_data.expiration_date - datetime.now()).days
        whois_data = vars(whois_data)
        whois_data["days_remaining"] = expiration_days
    except:
        print("Failed to calculate the expiration days")
        sys.exit(1)

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
        with open(args.file, "r") as domains:
            for domain_name in domains:
                whois_data = execute_whois(domain_name)
                print_whois(whois_data)
    elif args.domain:
        whois_data = execute_whois(args.domain)
        print_whois(whois_data)
        
if __name__ == "__main__":
    main()  