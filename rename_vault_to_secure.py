import os
import glob

# Walk through all Kotlin files
for root, dirs, files in os.walk("app/src/main/java"):
    for file in files:
        if file.endswith(".kt"):
            filepath = os.path.join(root, file)
            with open(filepath, "r") as f:
                content = f.read()
            
            # Change "Vault" to "Secure" for UI text
            # We should probably do it carefully to avoid breaking things, but since it's just a name, let's do case-sensitive replace
            content = content.replace('"Vault"', '"Secure"')
            content = content.replace('VaultScreen(', 'SecureScreen(')
            content = content.replace('fun VaultScreen(', 'fun SecureScreen(')
            
            # specific string replaces:
            content = content.replace('"Open Existing Vault"', '"Open Existing Secure"')
            content = content.replace('"Create New Vault"', '"Create New Secure"')
            content = content.replace('"Decrypting Vault..."', '"Decrypting Secure..."')
            content = content.replace('"Unlock Vault"', '"Unlock Secure"')
            content = content.replace('"Close Vault"', '"Close Secure"')
            
            # lower-case stuff
            content = content.replace('"vault"', '"secure"') # mainly for navigation routes
            
            # Also replace in sentences:
            content = content.replace('lock vault', 'lock secure')
            
            with open(filepath, "w") as f:
                f.write(content)

print("Renamed in KT files")
