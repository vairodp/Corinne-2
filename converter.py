
import sys


# replacement strings
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'

# relative or absolute file path, e.g.:
file_path = r"C:\Users\Vairo\Downloads\Corinne-master\gatto.gv"

with open(file_path, 'rb') as open_file:
    content = open_file.read()

content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)

with open(file_path, 'wb') as open_file:
    open_file.write(content)
#filename = sys.argv[1]
#text = open(filename, 'rb').read().replace('\r\n', '\n')
#open(filename, 'wb').write(text)