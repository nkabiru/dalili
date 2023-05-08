import fitz
from os import listdir
from os.path import isfile, join, splitext

src_dir = 'interruptions'
dest_dir = 'text'

files = [f for f in listdir(src_dir) if isfile(join(src_dir, f))]

for file in files:
    infile = fitz.open(join(src_dir, file))
    # Remove .pdf extension, and append .txt extension
    dest_filename = splitext(file)[0] + '.txt'
    outfile = open(join(dest_dir, dest_filename), 'wb')

    # Just in case the pdf has multiple pages
    for page in infile:
        text = page.get_text().encode('utf8')
        outfile.write(text)
        # Form feed / Page delimiter
        outfile.write(bytes((12,)))

    outfile.close()
    print(f"Write {dest_filename} completed")

# doc = fitz.open('interruptions/interruptions_20230420.pdf')

# out = open('text/interruptions_20230420.txt', 'wb')
# for page in doc:
#     text = page.get_text().encode('utf8')
#     out.write(text)
#     # Form feed / Page delimiter
#     out.write(bytes((12,)))

# out.close()
