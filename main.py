import os
import argparse
import requests
import simple_colors

def check_site(url, connectivity_type, ssl):
    """
    Checks the reachability of a site using the specified connectivity type (GET or POST) and SSL.

    Parameters:
    url (str): The URL of the site to check.
    connectivity_type (str): The type of connectivity check ('GET' or 'POST').
    ssl (bool): Whether to use SSL (True) or not (False).

    Returns:
    None
    """
    # Ensure the URL starts with http:// or https://
    if not url.startswith(('http://', 'https://')):
        url = ('https://' if ssl else 'http://') + url

    try:
        # Perform the connectivity check based on the specified type
        if connectivity_type.upper() == 'GET':
            response = requests.get(url)
        elif connectivity_type.upper() == 'POST':
            response = requests.post(url)
        else:
            print(simple_colors.red("Invalid connectivity type. Please choose 'GET' or 'POST'."))
            return

        # Detailed response status handling
        if response.status_code == 200:
            print(simple_colors.green(f"Site {url} is reachable with status code 200 (OK)."))
        elif response.status_code == 301:
            print(simple_colors.yellow(f"Site {url} has moved permanently with status code 301 (Moved Permanently)."))
        elif response.status_code == 302:
            print(simple_colors.yellow(f"Site {url} found with status code 302 (Found)."))
        elif response.status_code == 403:
            print(simple_colors.red(f"Site {url} access is forbidden with status code 403 (Forbidden)."))
        elif response.status_code == 404:
            print(simple_colors.red(f"Site {url} not found with status code 404 (Not Found)."))
        elif response.status_code == 500:
            print(simple_colors.red(f"Site {url} encountered an internal server error with status code 500 (Internal Server Error)."))
        else:
            print(simple_colors.yellow(f"Site {url} returned status code {response.status_code}."))
    except requests.ConnectionError:
        print(simple_colors.red(f"Site {url} is unreachable."))

def main():
    """
    Main function to parse arguments and check site connectivity.

    Returns:
    None
    """
    parser = argparse.ArgumentParser(description="Check site connectivity.")
    parser.add_argument('--url', required=True, type=str, help='URL to check for reachability')
    parser.add_argument('--type', required=True, choices=['GET', 'POST'], type=str, help='Type of connectivity check (GET or POST)')
    parser.add_argument('--ssl', required=True, choices=['yes', 'no'], type=str, help='Whether to use SSL (yes or no)')
    
    args = parser.parse_args()
    ssl = args.ssl.lower() == 'yes'
    
    check_site(args.url, args.type.upper(), ssl)

if __name__ == "__main__":
    main()
