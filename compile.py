with open('stats_handwritten.py', 'r') as f:
    source_code = f\
        .read()\
        .replace('\t', '')\
        .replace(' '*4, '')\
        .replace('\n', '')

with open('stats_compiled.py', 'w') as f:
    f.write(source_code)

