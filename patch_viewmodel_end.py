with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

# The file now ends with "}\n    fun updateEntry(..." so we need to move that brace to the end.
import re
match = re.search(r'}\s*fun updateEntry', content)
if match:
    # Remove the stray brace
    content = content[:match.start()] + "\n" + content[match.start()+1:] + "\n}\n"
    with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
        f.write(content)
