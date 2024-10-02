import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def scrape_chapter(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve chapter: {url}")
        return None, None, None, None, None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    chapter_parts = url.split('/')[-4:]

    if len(chapter_parts) < 4:
        print("Scraping finished")
        return None, None, None, None

    chapter_number, chapter_title = chapter_parts[2].capitalize().replace('-', ' '), chapter_parts[3].capitalize().replace('-', ' ')
    content = soup.find('div', class_='chapter-content')
    if content:
        paragraphs = content.find_all('p')
        chapter_content = "\n".join(p.text.strip() for p in paragraphs)
    else:
        print('Could not find chapter content')
        return None, None, None, None
    
    a_tags = soup.find_all('a')
    next_button = None
    for a in a_tags:
        text_content = a.get_text(strip=True)
        if text_content == "Next Chapter":
            next_button = a
            break

    if next_button:
        next_url = next_button['href'] if next_button and 'href' in next_button.attrs else None
    else:
        print("No next url found")
        return None, None, None, None

    if next_url and not next_url.startswith("http"):
        base_url = urlparse(url).scheme + "://" + urlparse(url).netloc 
        next_url = base_url + next_url

    return chapter_number, chapter_title, chapter_content, next_url

def save_chapter_to_file(chapter_number, chapter_title, chapter_content, volume_name):
    with open(f"{volume_name}.txt", 'a', encoding='utf-8') as file:
        file.write(f"{chapter_number} : {chapter_title}\n\n")
        file.write(chapter_content + '\n\n')

def scrape_light_novel(start_url):
    current_url = start_url
    pass_count = 0
    
    chapter_parts = start_url.split('/')[-4:]
    volume_name = chapter_parts[0].capitalize().replace('-', ' ')
    
    while current_url:
        print(f"Scraping {current_url}")
        chapter_number, chapter_title, chapter_content, next_url = scrape_chapter(current_url)
        pass_count += 1

        if pass_count == 1:
            if os.path.exists(f"{volume_name}.txt"):
                os.remove(f"{volume_name}.txt")

        if chapter_number and chapter_title and chapter_content:
            save_chapter_to_file(chapter_number, chapter_title, chapter_content, volume_name)
            current_url = next_url
        else:
            print("No more chapters")
            break
        
    return volume_name

def register_custom_fonts():
    regular_font_path = "fonts/DejaVuSans.ttf"
    bold_font_path = "fonts/DejaVuSans-Bold.ttf"
    pdfmetrics.registerFont(TTFont('DejaVuSans', regular_font_path))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', bold_font_path))

def convert_to_pdf(volume_name):
    pdf_filename = f"{volume_name}.pdf"
    txt_filename = f"{volume_name}.txt"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    register_custom_fonts()

    volume_style = ParagraphStyle(
        name='VolumeStyle',
        fontSize=20,
        fontName='DejaVuSans-Bold',
        textColor=colors.black,
        leading=24,
        spaceAfter=24
    )

    title_style = ParagraphStyle(
        name='TitleStyle',
        fontSize=16,
        fontName='DejaVuSans-Bold',
        textColor=colors.black,
        leading=20,
        spaceBefore=12,
        spaceAfter=18
    )

    custom_style = ParagraphStyle(
        name='CustomStyle',
        fontSize=12,
        fontName='DejaVuSans',
        textColor=colors.black,
        leading=18,
        spaceBefore=6,
        spaceAfter=12
    )

    content = []
    volume_paragraph = Paragraph(volume_name, volume_style)
    content.append(volume_paragraph)

    if os.path.exists(txt_filename):
        with open(txt_filename, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    if line.startswith("Chapter"):
                        chapter_paragraph = Paragraph(line.strip(), title_style)
                        content.append(chapter_paragraph)
                    elif line.startswith("Prologue"):
                        prologue_paragraph = Paragraph(line.strip(), title_style)
                        content.append(prologue_paragraph)
                    else:
                        paragraph = Paragraph(line.strip(), custom_style)
                        content.append(paragraph)

        doc.build(content)
        print(f"PDF created: {pdf_filename}")
        os.remove(txt_filename)
        print(f"Text file deleted: {txt_filename}")
    else:
        print(f"Text file not found: {txt_filename}")

if __name__ == '__main__':
    starting_url = input("Enter url : ")
    volume_name = scrape_light_novel(starting_url)
    convert_to_pdf(volume_name)
