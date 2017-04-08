import sys

lines = sys.stdin.readlines()
switch = True
footer_switch = True
new_lines = []
for line in lines:
    line = line.decode('utf-8')
    if len(line) >= 4 and line[:4] == u'\u6536\u7a3f\u65e5\u671f': # First page footer
        footer_switch = False
    if len(line) >= 7 and line[:7] == u'\x0cPage 2':
        footer_switch = True
    if len(line) > 0 and line[0] == '1':
        if line.replace(' ', '').strip('\r\n') == u'1\u5f15\u8a00': # Main body
            new_lines.append('==========\n')
            switch = True
    if switch and footer_switch:
        new_lines.append(line)
    if len(line) >= 3 and line[:3] == u'\u5173\u952e\u8bcd': #keyword
        switch = False

for i in range(len(new_lines)):
    line = new_lines[len(new_lines) - i - 1]
    if len(line) >= 4 and line[:4] == u'\u53c2\u8003\u6587\u732e': # remove reference
        new_lines = new_lines[:(len(new_lines) - i - 1)]
        break
for line in new_lines:
    sys.stdout.write(line.encode('utf-8'))
