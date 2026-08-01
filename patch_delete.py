with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    text = f.read()

delete_entry_old = """    fun deleteEntry(entry: Entry) {
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
                _hasUnsavedChanges.value = true
            }
        }
    }"""

delete_entry_new = """    fun deleteEntry(entry: Entry) {
        viewModelScope.launch(Dispatchers.Default) {
            val currentDb = _database.value ?: return@launch
            val parentUuid = findParentGroupUuidForEntry(currentDb.content.group, entry.uuid) ?: return@launch
            
            val updatedDb = currentDb.modifyGroup(parentUuid) {
                copy(entries = entries.filter { it.uuid != entry.uuid })
            }
            withContext(Dispatchers.Main) {
                _database.value = updatedDb
                val cg = _currentGroup.value
                if (cg?.uuid == parentUuid) {
                    _currentGroup.value = cg.copy(entries = cg.entries.filter { it.uuid != entry.uuid })
                } else if (cg != null) {
                    _currentGroup.value = findGroupById(updatedDb.content.group, cg.uuid) ?: updatedDb.content.group
                }
                _hasUnsavedChanges.value = true
            }
        }
    }"""

text = text.replace(delete_entry_old, delete_entry_new)

delete_group_old = """    fun deleteGroup(group: Group) {
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
                _hasUnsavedChanges.value = true
            }
        }
    }"""

delete_group_new = """    fun deleteGroup(group: Group) {
        viewModelScope.launch(Dispatchers.Default) {
            val currentDb = _database.value ?: return@launch
            val parentUuid = findParentGroupUuidForGroup(currentDb.content.group, group.uuid) ?: return@launch
            
            val updatedDb = currentDb.modifyGroup(parentUuid) {
                copy(groups = groups.filter { it.uuid != group.uuid })
            }
            withContext(Dispatchers.Main) {
                _database.value = updatedDb
                val cg = _currentGroup.value
                if (cg?.uuid == parentUuid) {
                    _currentGroup.value = cg.copy(groups = cg.groups.filter { it.uuid != group.uuid })
                } else if (cg != null) {
                    _currentGroup.value = findGroupById(updatedDb.content.group, cg.uuid) ?: updatedDb.content.group
                }
                _hasUnsavedChanges.value = true
            }
        }
    }"""

text = text.replace(delete_group_old, delete_group_new)

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "w") as f:
    f.write(text)
    
