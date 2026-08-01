import re

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    text = f.read()

# Add findParent functions
functions_to_add = """
    private fun findParentGroupUuidForEntry(group: app.keemobile.kotpass.models.Group, entryUuid: java.util.UUID): java.util.UUID? {
        if (group.entries.any { it.uuid == entryUuid }) return group.uuid
        for (sub in group.groups) {
            val res = findParentGroupUuidForEntry(sub, entryUuid)
            if (res != null) return res
        }
        return null
    }

    private fun findParentGroupUuidForGroup(group: app.keemobile.kotpass.models.Group, groupUuid: java.util.UUID): java.util.UUID? {
        if (group.groups.any { it.uuid == groupUuid }) return group.uuid
        for (sub in group.groups) {
            val res = findParentGroupUuidForGroup(sub, groupUuid)
            if (res != null) return res
        }
        return null
    }
    
    private fun findGroupById(group: app.keemobile.kotpass.models.Group, uuid: java.util.UUID): app.keemobile.kotpass.models.Group? {
        if (group.uuid == uuid) return group
        for (sub in group.groups) {
            val res = findGroupById(sub, uuid)
            if (res != null) return res
        }
        return null
    }
"""

# Replace in updateGroup
update_group_old = """    fun updateGroup(group: app.keemobile.kotpass.models.Group, name: String, iconName: String, color: String) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return"""

update_group_new = """    fun updateGroup(group: app.keemobile.kotpass.models.Group, name: String, iconName: String, color: String) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return
        val parentUuid = findParentGroupUuidForGroup(currentDb.content.group, group.uuid) ?: return"""

text = text.replace(update_group_old, update_group_new)

# Replace the save logic in updateGroup
update_group_save_old = """        val newCurrentGroup = currentGroup.copy(groups = currentGroup.groups.filter { it.uuid != group.uuid } + updatedGroup)
        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(groups = groups.filter { it.uuid != group.uuid } + updatedGroup)
        }
        _database.value = updatedDb
        _currentGroup.value = newCurrentGroup
        _hasUnsavedChanges.value = true"""

update_group_save_new = """        val updatedDb = currentDb.modifyGroup(parentUuid) {
            copy(groups = groups.filter { it.uuid != group.uuid } + updatedGroup)
        }
        _database.value = updatedDb
        if (_currentGroup.value?.uuid == parentUuid) {
            _currentGroup.value = _currentGroup.value?.copy(groups = _currentGroup.value!!.groups.filter { it.uuid != group.uuid } + updatedGroup)
        } else if (_currentGroup.value?.uuid == group.uuid) {
            _currentGroup.value = updatedGroup
        } else {
            // we might be inside a descendant, we can refresh currentGroup from db
            _currentGroup.value = findGroupById(updatedDb.content.group, _currentGroup.value!!.uuid) ?: updatedDb.content.group
        }
        _hasUnsavedChanges.value = true"""
        
text = text.replace(update_group_save_old, update_group_save_new)

# Now for updateEntry
update_entry_old = """    fun updateEntry(
        title: String,
        username: String,
        pass: String,
        url: String,
        notes: String,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>,
        hiddenFields: List<String> = emptyList(),
        tags: List<String> = emptyList()
    ) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return
        val entry = _currentEntry.value ?: return"""
        
update_entry_new = """    fun updateEntry(
        title: String,
        username: String,
        pass: String,
        url: String,
        notes: String,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>,
        hiddenFields: List<String> = emptyList(),
        tags: List<String> = emptyList()
    ) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return
        val entry = _currentEntry.value ?: return
        val parentUuid = findParentGroupUuidForEntry(currentDb.content.group, entry.uuid) ?: return"""

text = text.replace(update_entry_old, update_entry_new)

# Replace the save logic in updateEntry
update_entry_save_old = """        // Remove old entry and add new entry
        val updatedGroup = currentGroup.copy(entries = currentGroup.entries.filter { it.uuid != entry.uuid } + updatedEntry)
        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(entries = entries.filter { it.uuid != entry.uuid } + updatedEntry)
        }

        _database.value = updatedDb
        _currentGroup.value = updatedGroup
        _currentEntry.value = updatedEntry
        _hasUnsavedChanges.value = true"""

update_entry_save_new = """        // Remove old entry and add new entry
        val updatedDb = currentDb.modifyGroup(parentUuid) {
            copy(entries = entries.filter { it.uuid != entry.uuid } + updatedEntry)
        }

        _database.value = updatedDb
        if (_currentGroup.value?.uuid == parentUuid) {
            _currentGroup.value = _currentGroup.value?.copy(entries = _currentGroup.value!!.entries.filter { it.uuid != entry.uuid } + updatedEntry)
        } else {
            _currentGroup.value = findGroupById(updatedDb.content.group, _currentGroup.value!!.uuid) ?: updatedDb.content.group
        }
        _currentEntry.value = updatedEntry
        _hasUnsavedChanges.value = true"""

text = text.replace(update_entry_save_old, update_entry_save_new)

text = text.replace("}\n// end class", functions_to_add + "\n}\n// end class") # need to inject them

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "w") as f:
    f.write(text)

print("Patched!")
