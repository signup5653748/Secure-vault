import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

# Store password when unlocking
old_unlock = """    fun unlockDatabase(password: String) {
        val uri = _dbUri.value ?: return
        viewModelScope.launch(Dispatchers.IO) {"""

new_unlock = """    fun unlockDatabase(password: String) {
        val uri = _dbUri.value ?: return
        viewModelScope.launch(Dispatchers.IO) {
            val passStr = password"""

content = content.replace(old_unlock, new_unlock)

old_success = """                _database.value = db
                _currentGroup.value = db.content.group
                _error.value = null
            } catch (e: Exception) {"""

new_success = """                _database.value = db
                _currentGroup.value = db.content.group
                _error.value = null
                com.example.data.CryptoHelper.savePassword(context, passStr)
            } catch (e: Exception) {"""

content = content.replace(old_success, new_success)

# Remove the password when file is imported so they can't use biometric for new file unless saved
old_import = """    fun importFile(uri: Uri) {
        _database.value = null
        _currentGroup.value = null
        _currentEntry.value = null"""

new_import = """    fun importFile(uri: Uri) {
        com.example.data.CryptoHelper.clearPassword(context)
        _database.value = null
        _currentGroup.value = null
        _currentEntry.value = null"""

content = content.replace(old_import, new_import)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
