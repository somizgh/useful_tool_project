

import re
p=re.compile("asdf\?[0-9]+")
print(p.match("asdf?01"))