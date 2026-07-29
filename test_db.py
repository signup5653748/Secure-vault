with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    content = f.read()

import re
print(re.findall(r'val rootGroup = .*', content))
