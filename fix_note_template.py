with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    text = f.read()

import re

text = re.sub(r'BasicField\.Notes\(\) to EntryValue\.Plain\(""\),\n\s*"Note Content" to EntryValue\.Plain\(""\)', 'BasicField.Notes() to EntryValue.Plain("")', text)

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "w") as f:
    f.write(text)

print("Fixed Note template")
