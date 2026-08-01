with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    text = f.read()

duplicate_entry_old = """    fun duplicateEntry(entry: Entry) {
        val newFields = entry.fields.toMutableMap().apply {
            val titleField = app.keemobile.kotpass.constants.BasicField.Title()
            val oldTitle = get(titleField)?.content ?: "Unnamed"
            put(titleField, app.keemobile.kotpass.models.EntryValue.Plain("$oldTitle (Copy)"))
        }
        val newEntry = entry.copy(
            uuid = java.util.UUID.randomUUID(),
            fields = app.keemobile.kotpass.models.EntryFields(newFields)
        )
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.Default) {
            val currentGroupUuid = _currentGroup.value?.uuid ?: return@launch
            val updatedDb = _database.value?.modifyGroup(currentGroupUuid) {
                copy(entries = entries + newEntry)
            }
            if (updatedDb != null) {
                kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                    _database.value = updatedDb
                    _hasUnsavedChanges.value = true
                    _currentGroup.value = updatedDb.getGroup { it.uuid == currentGroupUuid }?.second ?: _currentGroup.value
                }
            }
        }
    }"""

duplicate_entry_new = """    fun duplicateEntry(entry: Entry) {
        val newFields = entry.fields.toMutableMap().apply {
            val titleField = app.keemobile.kotpass.constants.BasicField.Title()
            val oldTitle = get(titleField)?.content ?: "Unnamed"
            put(titleField, app.keemobile.kotpass.models.EntryValue.Plain("$oldTitle (Copy)"))
        }
        val newEntry = entry.copy(
            uuid = java.util.UUID.randomUUID(),
            fields = app.keemobile.kotpass.models.EntryFields(newFields)
        )
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.Default) {
            val currentDb = _database.value ?: return@launch
            val parentUuid = findParentGroupUuidForEntry(currentDb.content.group, entry.uuid) ?: return@launch
            val updatedDb = currentDb.modifyGroup(parentUuid) {
                copy(entries = entries + newEntry)
            }
            if (updatedDb != null) {
                kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                    _database.value = updatedDb
                    _hasUnsavedChanges.value = true
                    _currentGroup.value = findGroupById(updatedDb.content.group, _currentGroup.value!!.uuid) ?: updatedDb.content.group
                }
            }
        }
    }"""

text = text.replace(duplicate_entry_old, duplicate_entry_new)

duplicate_group_old = """    fun duplicateGroup(group: app.keemobile.kotpass.models.Group) {
        val newGroup = group.copy(
            uuid = java.util.UUID.randomUUID(),
            name = "${group.name} (Copy)"
        )
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.Default) {
            val currentGroupUuid = _currentGroup.value?.uuid ?: return@launch
            val updatedDb = _database.value?.modifyGroup(currentGroupUuid) {
                copy(groups = groups + newGroup)
            }
            if (updatedDb != null) {
                kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                    _database.value = updatedDb
                    _hasUnsavedChanges.value = true
                    _currentGroup.value = updatedDb.getGroup { it.uuid == currentGroupUuid }?.second ?: _currentGroup.value
                }
            }
        }
    }"""

duplicate_group_new = """    fun duplicateGroup(group: app.keemobile.kotpass.models.Group) {
        val newGroup = group.copy(
            uuid = java.util.UUID.randomUUID(),
            name = "${group.name} (Copy)"
        )
        viewModelScope.launch(kotlinx.coroutines.Dispatchers.Default) {
            val currentDb = _database.value ?: return@launch
            val parentUuid = findParentGroupUuidForGroup(currentDb.content.group, group.uuid) ?: return@launch
            val updatedDb = currentDb.modifyGroup(parentUuid) {
                copy(groups = groups + newGroup)
            }
            if (updatedDb != null) {
                kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.Main) {
                    _database.value = updatedDb
                    _hasUnsavedChanges.value = true
                    _currentGroup.value = findGroupById(updatedDb.content.group, _currentGroup.value!!.uuid) ?: updatedDb.content.group
                }
            }
        }
    }"""

text = text.replace(duplicate_group_old, duplicate_group_new)

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "w") as f:
    f.write(text)

