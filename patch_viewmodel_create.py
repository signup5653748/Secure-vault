import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

create_group_old = """        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(groups = groups + newGroup)
        }

        _database.value = updatedDb
        saveDatabase()"""
create_group_new = """        val updatedGroup = currentGroup.copy(groups = currentGroup.groups + newGroup)
        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(groups = groups + newGroup)
        }

        _database.value = updatedDb
        _currentGroup.value = updatedGroup
        saveDatabase()"""
content = content.replace(create_group_old, create_group_new)

create_entry_old = """        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(entries = entries + newEntry)
        }

        _database.value = updatedDb
        saveDatabase()"""
create_entry_new = """        val updatedGroup = currentGroup.copy(entries = currentGroup.entries + newEntry)
        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(entries = entries + newEntry)
        }

        _database.value = updatedDb
        _currentGroup.value = updatedGroup
        saveDatabase()"""
content = content.replace(create_entry_old, create_entry_new)

update_entry_old = """        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(entries = entries.filter { it.uuid != entry.uuid } + updatedEntry)
        }

        _database.value = updatedDb
        _currentEntry.value = updatedEntry
        saveDatabase()"""
update_entry_new = """        val updatedGroup = currentGroup.copy(entries = currentGroup.entries.filter { it.uuid != entry.uuid } + updatedEntry)
        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(entries = entries.filter { it.uuid != entry.uuid } + updatedEntry)
        }

        _database.value = updatedDb
        _currentGroup.value = updatedGroup
        _currentEntry.value = updatedEntry
        saveDatabase()"""
content = content.replace(update_entry_old, update_entry_new)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
