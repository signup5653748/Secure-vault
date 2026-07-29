import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("value is app.keemobile.kotpass.cryptography.EncryptedValue", "value is app.keemobile.kotpass.models.EntryValue.Encrypted")

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)
