import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace("import kotlinx.coroutines.launch\n", "import kotlinx.coroutines.launch\nimport kotlinx.coroutines.withContext\n")

old_save = """    fun saveDatabase() {
        val db = _database.value ?: return
        val uri = _dbUri.value ?: return
        viewModelScope.launch {
            try {
                context.contentResolver.openOutputStream(uri)?.use { outputStream ->
                    db.encode(outputStream)
                }
                val currentGroupUuid = _currentGroup.value?.uuid
                if (currentGroupUuid != null) {
                    _currentGroup.value = db.getGroup { it.uuid == currentGroupUuid }?.first ?: db.content.group
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }"""

new_save = """    fun saveDatabase() {
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
content = content.replace(old_save, new_save)

old_createGroup = """        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(groups = groups + newGroup)
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
        
        val newCurrentGroup = if (updatedDb.content.group.uuid == currentGroup.uuid) updatedDb.content.group else updatedDb.getGroup { it.uuid == currentGroup.uuid }?.first
        if (newCurrentGroup != null) {
            _currentGroup.value = newCurrentGroup
        }"""

new_createGroup = """        viewModelScope.launch(Dispatchers.Default) {
            val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
                copy(groups = groups + newGroup)
            }
            withContext(Dispatchers.Main) {
                _database.value = updatedDb
            }
            withContext(Dispatchers.IO) {
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
            withContext(Dispatchers.Main) {
                val newCurrentGroup = if (updatedDb.content.group.uuid == currentGroup.uuid) updatedDb.content.group else updatedDb.getGroup { it.uuid == currentGroup.uuid }?.first
                if (newCurrentGroup != null) {
                    _currentGroup.value = newCurrentGroup
                }
            }
        }"""
content = content.replace(old_createGroup, new_createGroup)

old_createEntry = """        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
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
        
        val newCurrentGroup = if (updatedDb.content.group.uuid == currentGroup.uuid) updatedDb.content.group else updatedDb.getGroup { it.uuid == currentGroup.uuid }?.first
        if (newCurrentGroup != null) {
            _currentGroup.value = newCurrentGroup
        }"""

content = content.replace(old_createEntry, new_createGroup.replace("groups + newGroup", "entries + newEntry"))

old_deleteEntry = """    fun deleteEntry(entry: Entry) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return
        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(entries = entries.filter { it.uuid != entry.uuid })
        }
        _database.value = updatedDb
        saveDatabase()
    }"""
new_deleteEntry = """    fun deleteEntry(entry: Entry) {
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
content = content.replace(old_deleteEntry, new_deleteEntry)

old_deleteGroup = """    fun deleteGroup(group: Group) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return
        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(groups = groups.filter { it.uuid != group.uuid })
        }
        _database.value = updatedDb
        saveDatabase()
    }"""
new_deleteGroup = """    fun deleteGroup(group: Group) {
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
content = content.replace(old_deleteGroup, new_deleteGroup)

old_deleteTemplate = """    fun deleteTemplate(entry: Entry) {
        val db = _database.value ?: return
        val templatesGroup = db.content.group.groups.find { it.name == "Templates" } ?: return
        val updatedDb = db.modifyGroup(templatesGroup.uuid) {
            copy(entries = entries.filter { it.uuid != entry.uuid })
        }
        _database.value = updatedDb
        saveDatabase()
    }"""
new_deleteTemplate = """    fun deleteTemplate(entry: Entry) {
        viewModelScope.launch(Dispatchers.Default) {
            val db = _database.value ?: return@launch
            val templatesGroup = db.content.group.groups.find { it.name == "Templates" } ?: return@launch
            val updatedDb = db.modifyGroup(templatesGroup.uuid) {
                copy(entries = entries.filter { it.uuid != entry.uuid })
            }
            withContext(Dispatchers.Main) {
                _database.value = updatedDb
                saveDatabase()
            }
        }
    }"""
content = content.replace(old_deleteTemplate, new_deleteTemplate)

old_addTemplate = """        viewModelScope.launch {
            val templatesGroup = getOrCreateTemplatesGroup()
            val updatedDb = _database.value!!.modifyGroup(templatesGroup.uuid) {
                copy(entries = entries + newEntry)
            }
            _database.value = updatedDb
            saveDatabase()
        }"""
new_addTemplate = """        viewModelScope.launch(Dispatchers.Default) {
            val templatesGroup = getOrCreateTemplatesGroup()
            val updatedDb = _database.value!!.modifyGroup(templatesGroup.uuid) {
                copy(entries = entries + newEntry)
            }
            withContext(Dispatchers.Main) {
                _database.value = updatedDb
                saveDatabase()
            }
        }"""
content = content.replace(old_addTemplate, new_addTemplate)

old_createEntryFromTemplate = """    fun createEntryFromTemplate(template: Entry) {
        val db = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return
        
        val newEntry = template.copy(uuid = java.util.UUID.randomUUID())
        val updatedDb = db.modifyGroup(currentGroup.uuid) {
            copy(entries = entries + newEntry)
        }
        _database.value = updatedDb
        saveDatabase()
    }"""
new_createEntryFromTemplate = """    fun createEntryFromTemplate(template: Entry) {
        viewModelScope.launch(Dispatchers.Default) {
            val db = _database.value ?: return@launch
            val currentGroup = _currentGroup.value ?: return@launch
            
            val newEntry = template.copy(uuid = java.util.UUID.randomUUID())
            val updatedDb = db.modifyGroup(currentGroup.uuid) {
                copy(entries = entries + newEntry)
            }
            withContext(Dispatchers.Main) {
                _database.value = updatedDb
                saveDatabase()
            }
        }
    }"""
content = content.replace(old_createEntryFromTemplate, new_createEntryFromTemplate)

old_getOrCreateSave = """            val updatedDb = db.modifyGroup(db.content.group.uuid) {
                copy(groups = groups + templatesGroup!!)
            }
            
            _database.value = updatedDb
            saveDatabase()"""
new_getOrCreateSave = """            withContext(Dispatchers.Default) {
                val updatedDb = db.modifyGroup(db.content.group.uuid) {
                    copy(groups = groups + templatesGroup!!)
                }
                withContext(Dispatchers.Main) {
                    _database.value = updatedDb
                    saveDatabase()
                }
            }"""
content = content.replace(old_getOrCreateSave, new_getOrCreateSave)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
