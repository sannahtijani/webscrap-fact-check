with open('20MinutesURL.txt', 'r') as f:
    lines = f.readlines()
    unique_lines = list(set(lines))
    with open('20MinutesURL.txt', 'w') as f:
        f.writelines(unique_lines)

import re

with open('20MinutesURL.txt', 'r') as f:
    lines = f.readlines()
    lines.sort(key=lambda x: int(re.search(r'\d+', x.split('-')[1]).group()) if re.search(r'\d+', x.split('-')[1]) else 0, reverse=True)
    with open('20MinutesURL.txt', 'w') as f:
        f.writelines(lines)
