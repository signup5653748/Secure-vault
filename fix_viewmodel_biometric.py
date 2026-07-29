import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

new_fun = """
    fun unlockWithSavedPassword(): Boolean {
        val savedPass = com.example.data.CryptoHelper.getPassword(context)
        if (savedPass != null) {
            unlockDatabase(savedPass)
            return true
        }
        return false
    }
"""

content = content.replace("fun importFile(uri: Uri) {", new_fun + "\n    fun importFile(uri: Uri) {")

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
