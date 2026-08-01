import os

# 1. Update metadata.json
with open("metadata.json", "r") as f:
    meta = f.read()
meta = meta.replace('"name": "Vault"', '"name": "secure"')
with open("metadata.json", "w") as f:
    f.write(meta)

# 2. Update strings.xml
with open("app/src/main/res/values/strings.xml", "r") as f:
    strings = f.read()
strings = strings.replace('<string name="app_name">Vault</string>', '<string name="app_name">secure</string>')
with open("app/src/main/res/values/strings.xml", "w") as f:
    f.write(strings)

# 3. Update settings.gradle.kts
with open("settings.gradle.kts", "r") as f:
    settings = f.read()
settings = settings.replace('rootProject.name = "Vault"', 'rootProject.name = "secure"')
with open("settings.gradle.kts", "w") as f:
    f.write(settings)

# 4. Update CreateDatabaseScreen.kt
with open("app/src/main/java/com/example/ui/CreateDatabaseScreen.kt", "r") as f:
    screen = f.read()
screen = screen.replace('var databaseName by remember { mutableStateOf("NewDatabase") }', 'var databaseName by remember { mutableStateOf("secure") }')
with open("app/src/main/java/com/example/ui/CreateDatabaseScreen.kt", "w") as f:
    f.write(screen)

print("Renamed to secure")
