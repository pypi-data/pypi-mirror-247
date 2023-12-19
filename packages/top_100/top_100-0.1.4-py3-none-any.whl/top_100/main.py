import requests
from top_100.extract_urls import ExtractUrls


def access_domains(top_100):
    """
    Access each domain in a list and print its response code.

    Parameters:
    top_100 (list): A list of dictionaries representing a table of domains.

    Returns:
    None
    """

    for entry in top_100:
        try:
            url = entry.get('Domainname')
            response = requests.get(url, timeout=5)
        except requests.exceptions.Timeout:
            print(f"The request for {url} timed out")
        except requests.exceptions.ConnectionError:
            print(f"domain: {url} connection error")
        except requests.exceptions.MissingSchema:
            print(f"url schema error: {url}")
        else:
            print(f"domain: {url} response code: {response.status_code}")


# Use the function
top_100_reference = "https://en.wikipedia.org/wiki/List_of_most-visited_websites"  # Replace with your URL
extract = ExtractUrls(top_100_reference)
extract.html_table_to_list()
access_domains(extract.data_list)
