import re

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    content = f.read()

# Add entry color/icon to view model

new_create_entry = """    fun createEntry(
        title: String,
        username: String,
        pass: String,
        url: String,
        notes: String,
        iconName: String = "Key",
        color: String = "Blue",
        customFields: List<Triple<String, String, Boolean>> = emptyList() // Name, Value, IsHidden
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
    }
"""

content = re.sub(r'    fun createEntry\([^)]*\)\s*\{[^}]*val updatedDb =.*?\}', new_create_entry, content, flags=re.DOTALL)
# oops the regex is bad because there's nested braces.

