import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

old_lock = """    fun lockDatabase() {
        _database.value = null
        _currentGroup.value = null
        _currentEntry.value = null
        _dbUri.value = null
        settings.setDatabaseUri(null)
    }"""

new_lock = """    fun lockDatabase() {
        if (settings.clipboardAutoClear.value) {
            try {
                val clipboard = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.P) {
                    clipboard.clearPrimaryClip()
                } else {
                    clipboard.setPrimaryClip(android.content.ClipData.newPlainText("", ""))
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        _database.value = null
        _currentGroup.value = null
        _currentEntry.value = null
    }"""

content = content.replace(old_lock, new_lock)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)

