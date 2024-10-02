# RoyalMTLS Light Novel Scraper and PDF Converter

This Python project allows you to scrape light novels from [RoyalMTLS](https://royalmtls.com/) website, save the scraped chapters into a text file, and then convert the content into a properly formatted PDF. The project supports custom fonts, handles special characters (such as `ō`), and automatically deletes the intermediate text file after generating the PDF.

## Features

- **Web Scraping:** Scrapes chapters of light novels from RoyalMTLS website using BeautifulSoup.
- **Automatic PDF Creation:** Converts the scraped content into a PDF, with custom formatting for chapter titles and body text.
- **Custom Font Support:** Uses DejaVu Sans fonts to properly render special characters and ensure clean text presentation.
- **Automated Cleanup:** Deletes the intermediate text file after the PDF has been generated.
- **Error Handling:** Gracefully handles issues like missing chapters or failed HTTP requests.

## Requirements

Ensure you have the following Python packages installed:

- `requests`
- `beautifulsoup4`
- `reportlab`

You can install them using the following command:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone the repository

```
git clone https://github.com/shivain2393/royalmtls-scraper.git
cd royalmtls-scraper
```

2. Install the required dependencies

```
pip install -r requirements.txt
```

## Usage

1. Run the scraper by executing the following command.

```
python scraper.py
```

2. When prompted, enter the URL of the first chapter of the light novel on RoyalMTLS website that you want to scrape.

3. The scraper will:
- Extract the content of each chapter.
- Save it to a text file named after the volume of the light novel.
- Convert the text file into a PDF with properly formatted titles and body text.
- Delete the text file after creating the PDF.

##  Example

After running the script and providing the starting URL of a light novel (preferably the prologue or the first chapter), the program will create a PDF named after the volume (e.g., Volume-1.pdf) containing all the scraped chapters.

## Contributing

Feel free to fork the repository and submit pull requests to contribute to the project. Any suggestions or bug reports are welcome!

## License

This project is open-source and available under the MIT License.