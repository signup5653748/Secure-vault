import sys

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    content = f.read()

target = """    fun createEntry(title: String, username: String, pass: String, url: String, notes: String) {
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

replacement = """    fun createEntry(
        title: String,
        username: String,
        pass: String,
        url: String,
        notes: String,
        iconName: String,
        color: String,
        customFields: List<Triple<String, String, Boolean>>
    ) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return
        
        val icon = try {
            PredefinedIcon.valueOf(iconName)
        } catch (e: Exception) {
            PredefinedIcon.Key
        }
        
        val fieldsMap = mutableMapOf<String, EntryValue>(
            BasicField.Title() to EntryValue.Plain(title),
            BasicField.UserName() to EntryValue.Plain(username),
            BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString(pass)),
            BasicField.Url() to EntryValue.Plain(url),
            BasicField.Notes() to EntryValue.Plain(notes)
        )
        
        for (field in customFields) {
            if (field.third) {
                fieldsMap[field.first] = EntryValue.Encrypted(EncryptedValue.fromString(field.second))
            } else {
                fieldsMap[field.first] = EntryValue.Plain(field.second)
            }
        }

        val newEntry = Entry(
            uuid = UUID.randomUUID(),
            icon = icon,
            customData = mapOf("ThemeColor" to CustomDataValue(color)),
            fields = EntryFields(fieldsMap)
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

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "w") as f:
        f.write(content)
else:
    print("Target not found")
    sys.exit(1)

