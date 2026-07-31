import sys

with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

target_group = """        // Save to file
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
        }"""
replacement_group = """        _hasUnsavedChanges.value = true"""

content = content.replace(target_group, replacement_group)

target_entry = """            withContext(Dispatchers.IO) {
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
            }"""
replacement_entry = """            withContext(Dispatchers.Main) {
                _hasUnsavedChanges.value = true
            }"""

content = content.replace(target_entry, replacement_entry)

with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
print("Removed direct disk writes from createGroup and createEntry")
