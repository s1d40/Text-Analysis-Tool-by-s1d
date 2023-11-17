# pylint:disable=W0612
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import unicodedata


def read_text_file(file_name):
    """
    Reads the content of a text file.
    :param file_name: Name of the file (without extension).
    :return: Content of the file as a string.
    """
    try:
        with open(file_name + '.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {file_name}.txt not found.")
        return ""

def fetch_text_from_web(url):
    """
    Fetches and returns text content from a given webpage URL.
    :param url: Webpage URL.
    :return: Text content from the webpage.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.text
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return ""

''''def clean_text(text):
   
    Cleans text by removing specific symbols and non-alphabetic characters.
    :param text: Text to be cleaned.
    :return: Cleaned text.
   
    text = re.sub(r'>>>', '', text)
    text = re.sub(r'[^A-Za-z\s]', '', text)
    return text '''

def split_content_into_words(content):
    """
    Splits content into words.
    :param content: String content to be split.
    :return: List of words.
    """
    words = []
    for line in content.split('|'):
        words.extend(line.split())
    return words

def count_frequency(word_list):
    """
    Counts the frequency of each word in a list.
    :param word_list: List of words.
    :return: Dictionary of word frequencies.
    """
    word_count = {}
    for word in word_list:
        word = word.lower()  # Optional: Convert words to lowercase for case-insensitive counting
        word_count[word] = word_count.get(word, 0) + 1
    return word_count

def create_dataframe_from_dict(word_dict):
    """
    Creates a pandas DataFrame from a dictionary and sorts it by frequency.
    :param word_dict: Dictionary with word frequencies.
    :return: Sorted DataFrame.
    """
    df = pd.DataFrame(list(word_dict.items()), columns=['Word', 'Frequency'])
    df['Rank'] = df['Frequency'].rank(ascending=False, method='min')
    return df.sort_values(by='Frequency', ascending=False)

def clean_text(text):
    """
    Cleans text by applying various transformations.
    :param text: Text to be cleaned.
    :return: Cleaned text.
    """
    # Convert to lowercase
    text = text.lower()

    # Remove unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    # Expand contractions (optional, requires a contractions expansion function)

    # Tokenize text
    words = word_tokenize(text)

    # Initialize stopwords set and stemmer
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()

    # Remove stop words and stem the words
    words = [stemmer.stem(word) for word in words if word not in stop_words and word.isalpha()]

    # Rejoin words into a single string
    return ' '.join(words)

def main():
    '''
    Main function to execute the script.
    Provides a menu for the user to choose      between parsing a URL or a text file.
   '''
    print("Welcome to the Text Analysis Tool!")
    print("This tool allows you to analyze text data from a website or a text file.")
    print("You can:")
    print("  - Extract text from a specified URL and analyze its word frequency.")
    print("  - Read a text file and analyze the frequency of words within it.")
    print("  - Optionally, save the analysis results to CSV and Excel files for further use.")
    print("Let's get started!\n")
    while True:
        print("\nOptions:")
        print("1. Parse text from a URL")
        print("2. Parse text from a text file")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1' or choice.lower() == 'url':
            url = input("Enter the URL to parse: ")
            
            ##fetching text data from url
            
            
            content = fetch_text_from_web(url)
            

            ##clean data before passing on
        
            content = clean_text(content)
            
            
            ##defining string for file name
            file_name = "web_content_" + re.sub(r'\W+', '_', url.split('//')[-1].split('/')[0])
            
            
            
        elif choice == '2' or choice.lower() in ['txt','text','file']:
            
            
            file_name = input("Enter the name of the text file (without extension): ")
            
            
            ##content variable gets text from file instrad of url and cleaning is applied
            
            
            content = clean_text(read_text_file(file_name))
        
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

        if content:
            word_list = split_content_into_words(content)
            word_count = count_frequency(word_list)
            df = create_dataframe_from_dict(word_count)

            # Ask if user wants to save the data
            save_option = input("Do you want to save the results to CSV and Excel files? (yes/no): ").lower()
            if save_option == 'yes':
                csv_file = file_name + '.csv'
                xlsx_file = file_name + '.xlsx'
                df.to_csv(csv_file, index=False)
                df.to_excel(xlsx_file, index=False)
                print(f"Data saved to {csv_file} and {xlsx_file}")
            else:
                print("Data not saved.")

            print(df.head())
        else:
            print("No content to process.")

if __name__ == '__main__':
    main(