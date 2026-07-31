import sys

with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

target = """    fun realSaveDatabase() {
        val db = _database.value ?: return
        val uri = _dbUri.value ?: return

        viewModelScope.launch(Dispatchers.IO) {
            try {
                context.contentResolver.openOutputStream(uri)?.use { outputStream ->
                    db.encode(outputStream)
                }
                val currentGroupUuid = _currentGroup.value?.uuid
                if (currentGroupUuid != null) {
                    val newGroup = db.getGroup { it.uuid == currentGroupUuid }?.first ?: db.content.group
                    withContext(Dispatchers.Main) {
                        _currentGroup.value = newGroup
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }"""

replacement = """    fun realSaveDatabase() {
        val db = _database.value ?: return
        val uri = _dbUri.value ?: return

        viewModelScope.launch(Dispatchers.IO) {
            try {
                val tempFile = java.io.File(context.cacheDir, "temp_db_${System.currentTimeMillis()}.kdbx")
                java.io.FileOutputStream(tempFile).use { fos ->
                    db.encode(fos)
                }
                
                try {
                    context.contentResolver.openOutputStream(uri, "wt")?.use { outputStream ->
                        java.io.FileInputStream(tempFile).use { fis ->
                            fis.copyTo(outputStream)
                        }
                    }
                } finally {
                    tempFile.delete()
                }
                
                val currentGroupUuid = _currentGroup.value?.uuid
                if (currentGroupUuid != null) {
                    val newGroup = db.getGroup { it.uuid == currentGroupUuid }?.first ?: db.content.group
                    withContext(Dispatchers.Main) {
                        _currentGroup.value = newGroup
                        _hasUnsavedChanges.value = false
                    }
                } else {
                    withContext(Dispatchers.Main) {
                        _hasUnsavedChanges.value = false
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }"""

if target in content:
    print("Found exact target!")
else:
    print("WARNING: Exact target not found. Trying regex or manual cut...")
    import re
    # We can regex it out
    content = re.sub(r'    fun realSaveDatabase\(\) \{.*?(?=    fun changeMasterPassword)', replacement + '\n', content, flags=re.DOTALL)
    if "temp_db_" in content:
        print("Regex replaced successfully")

with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
