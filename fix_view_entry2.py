import re

with open('/app/applet/app/src/main/java/com/example/ui/ViewEntryScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("binaryRef.hash.hash", "binaryRef.name")

with open('/app/applet/app/src/main/java/com/example/ui/ViewEntryScreen.kt', 'w') as f:
    f.write(content)
