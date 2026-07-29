import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

old_import = """    fun importFile(uri: Uri) {
        // Take persistable permission"""

new_import = """    fun importFile(uri: Uri) {
        _database.value = null
        _currentGroup.value = null
        _currentEntry.value = null
        // Take persistable permission"""

content = content.replace(old_import, new_import)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
