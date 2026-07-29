import re

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    content = f.read()

# Replace the whole createEntry function
new_create_entry = """    fun createEntry(title: String, username: String, pass: String, url: String, notes: String) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return

        val newEntry = Entry(
            uuid = UUID.randomUUID(),
            fields = EntryFields(
                mapOf(
                    BasicField.Title() to EntryValue.Plain(title),
                    BasicField.UserName() to EntryValue.Plain(username),
                    BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString(pass)),
                    BasicField.Url() to EntryValue.Plain(url),
                    BasicField.Notes() to EntryValue.Plain(notes)
                )
            )
        )

        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(entries = entries + newEntry)
        }
        _database.value = updatedDb
        
        // Save to file
        viewModelScope.launch {
            val uri = _dbUri.value
            if (uri != null) {
                try {
                    context.contentResolver.openOutputStream(uri)?.use { outputStream ->
                        updatedDb.encode(outputStream)
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }
        
        val newCurrentGroup = updatedDb.getGroup { it.uuid == currentGroup.uuid }?.first
        if (newCurrentGroup != null) {
            _currentGroup.value = newCurrentGroup
        }
    }"""

# Use regex to find and replace createEntry
content = re.sub(r"    fun createEntry\(.*?\n    }", new_create_entry, content, flags=re.MULTILINE|re.DOTALL)

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "w") as f:
    f.write(content)
