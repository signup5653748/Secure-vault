with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    content = f.read()

# Add a function to get templates group, creating it if necessary
patch = """
    suspend fun getOrCreateTemplatesGroup(): app.keemobile.kotpass.models.Group {
        val db = _database.value ?: throw IllegalStateException("Database not loaded")
        var templatesGroup = db.content.group.groups.find { it.name == "Templates" }
        if (templatesGroup == null) {
            templatesGroup = app.keemobile.kotpass.models.Group(
                uuid = java.util.UUID.randomUUID(),
                name = "Templates",
                icon = app.keemobile.kotpass.models.PredefinedIcon.FolderInfo
            )
            
            val gmailTemplate = Entry(
                uuid = java.util.UUID.randomUUID(),
                icon = app.keemobile.kotpass.models.PredefinedIcon.EMail,
                fields = EntryFields(mutableMapOf(
                    BasicField.Title() to EntryValue.Plain("Gmail"),
                    BasicField.UserName() to EntryValue.Plain(""),
                    BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString("")),
                    BasicField.Url() to EntryValue.Plain("https://mail.google.com")
                ))
            )
            val noteTemplate = Entry(
                uuid = java.util.UUID.randomUUID(),
                icon = app.keemobile.kotpass.models.PredefinedIcon.Note,
                fields = EntryFields(mutableMapOf(
                    BasicField.Title() to EntryValue.Plain("Note"),
                    BasicField.Notes() to EntryValue.Plain("")
                )),
                customData = mapOf("TemplateType" to app.keemobile.kotpass.models.CustomDataValue("Note"))
            )
            
            templatesGroup = templatesGroup.copy(entries = listOf(gmailTemplate, noteTemplate))
            
            val updatedDb = db.modifyGroup(db.content.group.uuid) {
                copy(groups = groups + templatesGroup!!)
            }
            _database.value = updatedDb
            saveDatabase()
        }
        return templatesGroup
    }
    
    fun getTemplates(): List<Entry> {
        val db = _database.value ?: return emptyList()
        val templatesGroup = db.content.group.groups.find { it.name == "Templates" }
        return templatesGroup?.entries ?: emptyList()
    }
    
    fun deleteTemplate(entry: Entry) {
        val db = _database.value ?: return
        val templatesGroup = db.content.group.groups.find { it.name == "Templates" } ?: return
        val updatedDb = db.modifyGroup(templatesGroup.uuid) {
            copy(entries = entries.filter { it.uuid != entry.uuid })
        }
        _database.value = updatedDb
        saveDatabase()
    }
    
    fun addTemplate(title: String, username: String, pass: String, url: String, notes: String, iconName: String, color: String, customFields: List<Triple<String, String, Boolean>>) {
        val icon = try { app.keemobile.kotpass.models.PredefinedIcon.valueOf(iconName) } catch (e: Exception) { app.keemobile.kotpass.models.PredefinedIcon.Key }
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
            uuid = java.util.UUID.randomUUID(),
            icon = icon,
            customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue(color)),
            fields = EntryFields(fieldsMap)
        )
        viewModelScope.launch {
            val templatesGroup = getOrCreateTemplatesGroup()
            val updatedDb = _database.value!!.modifyGroup(templatesGroup.uuid) {
                copy(entries = entries + newEntry)
            }
            _database.value = updatedDb
            saveDatabase()
        }
    }
    
    fun createEntryFromTemplate(template: Entry) {
        val db = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return
        
        val newEntry = template.copy(uuid = java.util.UUID.randomUUID())
        val updatedDb = db.modifyGroup(currentGroup.uuid) {
            copy(entries = entries + newEntry)
        }
        _database.value = updatedDb
        saveDatabase()
    }
    
    fun saveDatabase() {
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
    }
"""

content = content.replace("fun isRootGroup(): Boolean {", patch + "\n    fun isRootGroup(): Boolean {")

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "w") as f:
    f.write(content)
