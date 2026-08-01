with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    text = f.read()

import re
matches = re.findall(r"fun .*?\(.*?\).*?\{", text)
for m in matches:
    print(m)
