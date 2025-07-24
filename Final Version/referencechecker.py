# Imports re module - regular expressions - used to match references to a style based on regex
# pattern. Imports requests module - used to interact with Elsevier API by fetching from URL
# Imports document class from python-docx library - used to open and ead  from an imported Word document

import re 
import requests
from docx import Document

# Elsevier Scopus API authenticater key

elsevier_API = "cd3878b02038af882ddb46a188baa280"

# Pattern dictionary used to hold regex patterns for each reference style format - such as Harvard and APA
# Each regex has named groups using ?P to gather each reference part
# Regex pattern breakdowns:
# Author: [A-Za-z\-']+, = a last name with letters, hyphens, or apostrophes followed by a comma
#         [A-Za-z]\.? = one initial letter, optionally followed by a full stop
#         ? = optional space
#         (?:[A-Za-z]\.?)* = optionally more initials 
#         \s+ = one or more spaces
# Year:   \( and \) = brackets around the year
#         (?P<year>\d{4}) = named year with exactly 4 digits
#         \.? = optional full stop after the year
#         \s+ = one or more spaces
# Title and Source:  \" = starting quotation
#         (?P<title>.+?) = one or more character
#         \"\. = closing quote followed by a full stop
#         \s+ = one or more spaces

patterns = {
    "Harvard": re.compile(
        r"^(?P<authors>[A-Za-z\-']+, [A-Za-z]\.? ?(?:[A-Za-z]\.?)*)\s+"
        r"\((?P<year>\d{4})\)\.?\s+"    
        r"\"(?P<title>.+?)\"\.\s+"
        r"(?P<source>.+)\.$"
    ),
    "APA": re.compile(
        r"^(?P<authors>([A-Za-z\-']+, [A-Za-z]\.? ?(?:[A-Za-z]\.?)*\s*(?:,| and | & )?\s*)+)"
        r"\((?P<year>\d{4})\)\.?\s+"    
        r"\"(?P<title>.+?)\"\.\s+"
        r"(?P<source>.+)\.$"
    ),
}
# Function that accepts single parameter - reference aa a string
# For loop to iterate over pattern dictionary - style is Harvard or APA
# pattern.match checks if entire string matches a regex pattern
# If so, becomes match object. If not, object is None
# If matched, extract named groups and style and create new dictionary. Return None otherwise

def parse_reference(reference):
    for style, pattern in patterns.items():
        match = pattern.match(reference)
        if match:
            return {
                "style": style,
                "authors": match.group("authors"),
                "year": match.group("year"),
                "title": match.group("title"),
                "source": match.group("source"),
            }
    return None

# Function that takes one parameter - reference as string
# Uses parse_reference function from earlier to parse
# If no reference style found, returned unrecognised format
# If found, return reference style with string

def format_reference_style(reference):
    parsed = parse_reference(reference)
    if not parsed:
        return f"Unrecognized format"
    return f"{parsed['style']} - {parsed['authors']} ({parsed['year']}). \"{parsed['title']}\". {parsed['source']}."

# Function takes four parameters - title which is required than optional others
# Always search by title and then by optional if they are available using if function
# Query joins all available as one string to search
# API endpoint specialised by URL, headers requests a JSON response, params contains necessary
# Query ane API required
# GET request made to Scopus APi, with headers and params now passed
# If 200 (successful) parse JSON response to Python dictionary
# Extracts structre of search results
# Takes first result only as likely to be best match and formats all details available
# Otherwise, prints no matches
# If response not 200, print HTTP error match

def check_reference_in_scopus(title, author=None, source=None, year=None):
    query_parts = [f'TITLE("{title}")']
    if author:
        query_parts.append(f'AUTH("{author}")')
    if source:
        query_parts.append(f'SRCTITLE("{source}")')
    if year:
        query_parts.append(f'PUBYEAR IS {year}')
    
    query = " AND ".join(query_parts)

    url = "https://api.elsevier.com/content/search/scopus"
    headers = {
        "Accept": "application/json"
    }
    params = {
        "query": query,
        "apiKey": elsevier_API
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        entries = data.get("search-results", {}).get("entry", [])
        if entries:
            result = entries[0]
            print("Reference found in Scopus:")
            print(f"Title   : {result.get('dc:title')}")
            print(f"Authors : {result.get('dc:creator')}")
            print(f"Journal : {result.get('prism:publicationName')}")
            print(f"Year    : {result.get('prism:coverDate', '')[:4]}")
            print(f"DOI     : {result.get('prism:doi')}")
        else:
            print("No match found in Scopus.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Asks user to enter docx name
# Uses Document class from library to open the file - File must be in same folder as using local path
# Currently marked flase as References heading not found
# Each reference stored in list

doc = Document(input("Enter a '.docx' file: "))
found = False
references = []

# Loops through each paragraph and removed leading whitespace
# Once references found, mark as True and skip that line
# All non empty lines are collected and added to list

for para in doc.paragraphs:
    text = para.text.strip()
    if text.lower() == "references":
        found = True
        continue
    if found and text:
        references.append(text)

# Loop through list
# Print original reference
# Uses previous function to gather reference style
# Parse reference into each category
# Once parsed, call check in scopus function - only uses first authors surname to simplify query
# If not found, user is told
for ref in references:
    print("--")
    print("Original Reference:", ref)
    formatted = format_reference_style(ref)
    print("Reference Style:", formatted)

    parsed = parse_reference(ref)
    if parsed:
        print("Checking in Scopus...")
        check_reference_in_scopus(
            title=parsed['title'],
            author=parsed['authors'].split(",")[0],  
            source=parsed['source'],
            year=parsed['year']
        )
    else:
        print("Could not find reference.")
