import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

delete_entry_old = """    fun deleteEntry(entry: Entry) {
        viewModelScope.launch(Dispatchers.Default) {
            val currentDb = _database.value ?: return@launch
            val currentGroup = _currentGroup.value ?: return@launch
            val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
                copy(entries = entries.filter { it.uuid != entry.uuid })
            }
            withContext(Dispatchers.Main) {
                _database.value = updatedDb
                saveDatabase()
            }
        }
    }"""
delete_entry_new = """    fun deleteEntry(entry: Entry) {
        viewModelScope.launch(Dispatchers.Default) {
            val currentDb = _database.value ?: return@launch
            val currentGroup = _currentGroup.value ?: return@launch
            val updatedGroup = currentGroup.copy(entries = currentGroup.entries.filter { it.uuid != entry.uuid })
            val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
                copy(entries = entries.filter { it.uuid != entry.uuid })
            }
            withContext(Dispatchers.Main) {
                _database.value = updatedDb
                _currentGroup.value = updatedGroup
                saveDatabase()
            }
        }
    }"""
content = content.replace(delete_entry_old, delete_entry_new)

delete_group_old = """    fun deleteGroup(group: Group) {
        viewModelScope.launch(Dispatchers.Default) {
            val currentDb = _database.value ?: return@launch
            val currentGroup = _currentGroup.value ?: return@launch
            val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
                copy(groups = groups.filter { it.uuid != group.uuid })
            }
            withContext(Dispatchers.Main) {
                _database.value = updatedDb
                saveDatabase()
            }
        }
    }"""
delete_group_new = """    fun deleteGroup(group: Group) {
        viewModelScope.launch(Dispatchers.Default) {
            val currentDb = _database.value ?: return@launch
            val currentGroup = _currentGroup.value ?: return@launch
            val updatedGroup = currentGroup.copy(groups = currentGroup.groups.filter { it.uuid != group.uuid })
            val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
                copy(groups = groups.filter { it.uuid != group.uuid })
            }
            withContext(Dispatchers.Main) {
                _database.value = updatedDb
                _currentGroup.value = updatedGroup
                saveDatabase()
            }
        }
    }"""
content = content.replace(delete_group_old, delete_group_new)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
