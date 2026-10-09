import filetype

filepath = r'E:\ChromeDownloads\cn-additional-list.txt'

with open(filepath, 'rb') as fopen:
    # https://pypi.org/project/filetype/
    mime_type = filetype.guess_mime(fopen.read(2048))

print(mime_type)   # None
