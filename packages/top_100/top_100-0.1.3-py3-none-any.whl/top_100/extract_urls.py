from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


def is_valid_url(url):
    """
    Check if the url is valid.

    Parameters:
    url (str): The url to be checked.

    Returns:
    bool: True if valid, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def html_table_to_list(url, num_columns=6):
    """
    Convert an HTML table to a list of dictionaries.

    Parameters:
    url (str): The url of the webpage containing the table.
    num_columns (int): The number of columns in the table.

    Returns:
    list: A list of dictionaries representing the table.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first table on the page
    table = soup.find_all('table')[0]

    # Get the headers of the table
    headers = [header.text.replace(' ', '').strip() for header in table.find_all('th')]

    # Get all the rows of the table
    rows = table.find_all('tr')

    # List to hold all data for JSON
    data_list = []

    # Go through each row
    for row in rows:
        data_dict = {}
        columns = row.find_all('td')
        # Only process rows with exactly num_columns columns
        if len(columns) == num_columns:
            # For each row, get each column
            for i, column in enumerate(columns):
                # Strip all whitespace, carriage return and line feed from each column
                column_text = "".join(column.text.split())
                # Prefix each value in the second column with "https://"
                if i == 1:
                    if column_text is None:
                        break
                    column_text = 'https://' + column_text
                    if not is_valid_url(column_text):
                        break
                data_dict[headers[i]] = column_text
            else:  # Only executed if the loop didn't break
                data_list.append(data_dict)

    return data_list
