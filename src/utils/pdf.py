import PyPDF2


def read(file_path, start_page, end_page):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        if num_pages < end_page:
            start_page = num_pages - end_page if num_pages - end_page > 0 else 0
            end_page = num_pages

        extracted_text = ""
        for page_num in range(start_page, end_page):
            page = reader.pages[page_num]
            extracted_text += page.extract_text()
        return extracted_text
