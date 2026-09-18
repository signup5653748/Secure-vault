package com.example.viewmodel

import android.app.Application
import android.content.Intent
import android.net.Uri
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.KeePassHelper
import com.example.data.SettingsRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

import app.keemobile.kotpass.database.getGroup
import app.keemobile.kotpass.models.CustomDataValue
import app.keemobile.kotpass.constants.PredefinedIcon
import java.util.UUID
import app.keemobile.kotpass.database.modifiers.modifyGroup
import app.keemobile.kotpass.models.Entry
import app.keemobile.kotpass.models.EntryFields
import app.keemobile.kotpass.models.EntryValue
import app.keemobile.kotpass.database.encode
import app.keemobile.kotpass.cryptography.EncryptedValue
import app.keemobile.kotpass.constants.BasicField
import app.keemobile.kotpass.models.Group
import app.keemobile.kotpass.database.KeePassDatabase
import com.example.ui.GroupDestination

class KeePassViewModel(application: Application) : AndroidViewModel(application) {

    private val context = application.applicationContext
    val settings = SettingsRepository(context)
    private var currentMasterPassword: String? = null
    
    fun setEnableBiometrics(enabled: Boolean) {
        settings.setEnableBiometrics(enabled)
        if (enabled) {
            currentMasterPassword?.let { com.example.data.CryptoHelper.savePassword(context, it) }
        } else {
            com.example.data.CryptoHelper.clearPassword(context)
        }
    }

    private val _dbUri = MutableStateFlow<Uri?>(null)
    val dbUri: StateFlow<Uri?> = _dbUri
    
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _database = MutableStateFlow<KeePassDatabase?>(null)
    val database: StateFlow<KeePassDatabase?> = _database.asStateFlow()

    private val _hasUnsavedChanges = MutableStateFlow(false)
    val hasUnsavedChanges: StateFlow<Boolean> = _hasUnsavedChanges.asStateFlow()

    private val _currentGroup = MutableStateFlow<Group?>(null)
    val currentGroup: StateFlow<Group?> = _currentGroup.asStateFlow()

    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()

    private val _searchResults = MutableStateFlow<List<app.keemobile.kotpass.models.Entry>>(emptyList())
    val searchResults: StateFlow<List<app.keemobile.kotpass.models.Entry>> = _searchResults.asStateFlow()

    fun setSearchQuery(query: String) {
        _searchQuery.value = query
        if (query.isEmpty()) {
            _searchResults.value = emptyList()
        } else {
            viewModelScope.launch(Dispatchers.Default) {
                val db = _database.value
                if (db != null) {
                    val allEntries = mutableListOf<app.keemobile.kotpass.models.Entry>()
                    fun traverse(group: app.keemobile.kotpass.models.Group) {
                        allEntries.addAll(group.entries.filter {
                            val title = it[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: ""
                            val user = it[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: ""
                            val url = it[app.keemobile.kotpass.constants.BasicField.Url]?.content ?: ""
                            title.contains(query, ignoreCase = true) || user.contains(query, ignoreCase = true) || url.contains(query, ignoreCase = true)
                        })
                        group.groups.forEach { traverse(it) }
                    }
                    traverse(db.content.group)
                    _searchResults.value = allEntries
                }
            }
        }
    }


    private val _currentEntry = MutableStateFlow<Entry?>(null)
    val currentEntry: StateFlow<Entry?> = _currentEntry.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    init {
        checkExistingUri()
    }

    private fun checkExistingUri() {
        settings.databaseUri.value?.let {
            _dbUri.value = Uri.parse(it)
        }
    }

    
    fun getMasterPassword(): String {
        return currentMasterPassword ?: com.example.data.CryptoHelper.getPassword(context) ?: ""
    }

    fun unlockWithSavedPassword(): Boolean {
        val savedPass = com.example.data.CryptoHelper.getPassword(context)
        if (savedPass != null) {
            unlockDatabase(savedPass)
            return true
        }
        return false
    }

    fun importFile(uri: Uri) {
        com.example.data.CryptoHelper.clearPassword(context)
        currentMasterPassword = null
        _database.value = null
        _currentGroup.value = null
        _currentEntry.value = null
        // Take persistable permission
        try {
            val takeFlags: Int = Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION
            context.contentResolver.takePersistableUriPermission(uri, takeFlags)
        } catch (e: Throwable) {
            e.printStackTrace()
        }
        _dbUri.value = uri
        settings.setDatabaseUri(uri.toString())
        _error.value = null
    }

    fun unlockDatabase(password: String) {
        viewModelScope.launch {
            _isLoading.value = true
            val uri = _dbUri.value
            if (uri != null) {
                try {
                    val db = KeePassHelper.loadDatabase(context, uri, password)
                    if (db != null) {
                        _database.value = db
                        _currentGroup.value = db.content.group
                        _error.value = null
                        currentMasterPassword = password
                        if (settings.enableBiometrics.value) {
                            com.example.data.CryptoHelper.savePassword(context, password)
                        }
                    } else {
                        _error.value = "Failed to unlock database. Incorrect password or invalid file."
                    }
                } catch (e: Exception) {
                    _error.value = "Error: ${e.message}"
                } finally {
                    _isLoading.value = false
                }
            } else {
                _error.value = "No database file selected."
                _isLoading.value = false
            }
        }
    }

    fun createDatabase(uri: Uri, password: String, onComplete: (Boolean, String?) -> Unit) {
        viewModelScope.launch {
            // Take persistable permission
            try {
                val takeFlags: Int = Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                context.contentResolver.takePersistableUriPermission(uri, takeFlags)
            } catch (e: Throwable) {
                e.printStackTrace()
            }
            
            val (success, errorMsg) = KeePassHelper.createNewDatabase(context, uri, password)
            if (success) {
                _dbUri.value = uri
                settings.setDatabaseUri(uri.toString())
                
                try {
                    val db = KeePassHelper.loadDatabase(context, uri, password)
                    if (db != null) {
                        _database.value = db
                        _currentGroup.value = db.content.group
                        _error.value = null
                        currentMasterPassword = password
                        if (settings.enableBiometrics.value) {
                            com.example.data.CryptoHelper.savePassword(context, password)
                        }
                    } else {
                        _error.value = "Failed to unlock database after creation."
                    }
                } catch (e: Exception) {
                    _error.value = "Error: ${e.message}"
                }
            }
            onComplete(success, errorMsg)
        }
    }

    fun selectGroup(group: Group) {
        _currentGroup.value = group
    }

    fun navigateUp() {
        val currentGroupUuid = _currentGroup.value?.uuid ?: return
        val parent = _database.value?.getGroup { it.uuid == currentGroupUuid }?.first
        if (parent != null) {
            _currentGroup.value = parent
        }
    }

        private val _selectedTemplate = MutableStateFlow<Entry?>(null)
    val selectedTemplate = _selectedTemplate.asStateFlow()

    fun selectTemplateForNewEntry(template: Entry?) {
        _selectedTemplate.value = template
    }

    fun selectEntry(entry: Entry) {
        _currentEntry.value = entry
    }

    fun clearError() {
        _error.value = null
    }
    
    

    fun updateGroup(group: app.keemobile.kotpass.models.Group, name: String, iconName: String, color: String) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return
        val parentUuid = findParentGroupUuidForGroup(currentDb.content.group, group.uuid) ?: return
        val icon = try {
            app.keemobile.kotpass.constants.PredefinedIcon.valueOf(iconName)
        } catch (e: Exception) {
            app.keemobile.kotpass.constants.PredefinedIcon.Folder
        }
        val updatedGroup = group.copy(
            name = name,
            icon = icon,
            customData = group.customData.toMutableMap().apply {
                put("ThemeColor", app.keemobile.kotpass.models.CustomDataValue(color))
            }
        )
        val updatedDb = currentDb.modifyGroup(parentUuid) {
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
        _hasUnsavedChanges.value = true
    }

    fun createGroup(name: String, iconName: String, color: String) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return

        val icon = try {
            PredefinedIcon.valueOf(iconName)
        } catch (e: Exception) {
            PredefinedIcon.Folder
        }

        val newGroup = Group(
            uuid = UUID.randomUUID(),
            name = name,
            icon = icon,
            customData = mapOf("ThemeColor" to CustomDataValue(color))
        )

        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(groups = groups + newGroup)
        }
        _database.value = updatedDb
        
        _hasUnsavedChanges.value = true
        
        // Update current group to trigger recompose
        val newCurrentGroup = if (updatedDb.content.group.uuid == currentGroup.uuid) updatedDb.content.group else updatedDb.getGroup { it.uuid == currentGroup.uuid }?.second
        if (newCurrentGroup != null) {
            _currentGroup.value = newCurrentGroup
        }
    }

    fun createEntry(
        title: String,
        username: String?,
        pass: String?,
        url: String?,
        notes: String?,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>,
        tags: List<String> = emptyList()
    ) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return
        
        val icon = try {
            PredefinedIcon.valueOf(iconName)
        } catch (e: Exception) {
            PredefinedIcon.Key
        }
        
        val fieldsMap = mutableMapOf<String, EntryValue>()
        fieldsMap[BasicField.Title()] = EntryValue.Plain(title)
        if (username != null) fieldsMap[BasicField.UserName()] = EntryValue.Plain(username)
        if (pass != null) fieldsMap[BasicField.Password()] = EntryValue.Encrypted(EncryptedValue.fromString(pass))
        if (url != null) fieldsMap[BasicField.Url()] = EntryValue.Plain(url)
        if (notes != null) fieldsMap[BasicField.Notes()] = EntryValue.Plain(notes)
        
        for (field in customFields) {
            if (field.isHidden) {
                fieldsMap[field.name] = EntryValue.Encrypted(EncryptedValue.fromString(field.value))
            } else {
                fieldsMap[field.name] = EntryValue.Plain(field.value)
            }
        }

        val newEntry = Entry(
            uuid = UUID.randomUUID(),
            icon = icon,
            tags = tags,
            backgroundColor = color, foregroundColor = "#FFFFFF",
            customData = mapOf("ThemeColor" to CustomDataValue(color)) + customFields.associate { "ShowCopyButton_${it.name}" to CustomDataValue(it.showCopyButton.toString()) },
            fields = EntryFields(fieldsMap)
        )
        viewModelScope.launch(Dispatchers.Default) {
            val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
                copy(entries = entries + newEntry)
            }
            withContext(Dispatchers.Main) {
                _database.value = updatedDb
            }
            withContext(Dispatchers.Main) {
                _hasUnsavedChanges.value = true
            }
            withContext(Dispatchers.Main) {
                val newCurrentGroup = if (updatedDb.content.group.uuid == currentGroup.uuid) updatedDb.content.group else updatedDb.getGroup { it.uuid == currentGroup.uuid }?.second
                if (newCurrentGroup != null) {
                    _currentGroup.value = newCurrentGroup
                }
            }
        }
    }

    
    suspend fun getOrCreateTemplatesGroup(): app.keemobile.kotpass.models.Group {
        val db = _database.value ?: throw IllegalStateException("Database not loaded")
        var templatesGroup = db.content.group.groups.find { it.name == "Templates" }
        
        if (templatesGroup == null) {
            val predefinedTemplates = listOf(
                Entry(
                    uuid = java.util.UUID.randomUUID(),
                    icon = app.keemobile.kotpass.constants.PredefinedIcon.Email,
                    customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Red")),
                    fields = EntryFields(mutableMapOf(
                        BasicField.Title() to EntryValue.Plain("Gmail"),
                        BasicField.UserName() to EntryValue.Plain(""),
                        BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString("")),
                        BasicField.Url() to EntryValue.Plain("https://mail.google.com")
                    ))
                ),
                Entry(
                    uuid = java.util.UUID.randomUUID(),
                    icon = app.keemobile.kotpass.constants.PredefinedIcon.NetworkServer,
                    customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Blue")),
                    fields = EntryFields(mutableMapOf(
                        BasicField.Title() to EntryValue.Plain("Facebook"),
                        BasicField.UserName() to EntryValue.Plain(""),
                        BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString("")),
                        BasicField.Url() to EntryValue.Plain("https://facebook.com")
                    ))
                ),
                Entry(
                    uuid = java.util.UUID.randomUUID(),
                    icon = app.keemobile.kotpass.constants.PredefinedIcon.World,
                    customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Cyan")),
                    fields = EntryFields(mutableMapOf(
                        BasicField.Title() to EntryValue.Plain("Twitter"),
                        BasicField.UserName() to EntryValue.Plain(""),
                        BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString("")),
                        BasicField.Url() to EntryValue.Plain("https://twitter.com")
                    ))
                ),
                Entry(
                    uuid = java.util.UUID.randomUUID(),
                    icon = app.keemobile.kotpass.constants.PredefinedIcon.Money,
                    customData = mapOf(
                        "ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Green"),
                        "Hide_Url" to app.keemobile.kotpass.models.CustomDataValue("true"),
                        "Hide_UserName" to app.keemobile.kotpass.models.CustomDataValue("true"),
                        "Hide_Password" to app.keemobile.kotpass.models.CustomDataValue("true"),
                        "Hide_Notes" to app.keemobile.kotpass.models.CustomDataValue("true")
                    ),
                    fields = EntryFields(mutableMapOf(
                        BasicField.Title() to EntryValue.Plain("Bank Account"),
                        BasicField.UserName() to EntryValue.Plain(""),
                        BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString("")),
                        BasicField.Url() to EntryValue.Plain(""),
                        BasicField.Notes() to EntryValue.Plain(""),
                        "Account Number" to EntryValue.Encrypted(EncryptedValue.fromString("")),
                        "Routing Number" to EntryValue.Encrypted(EncryptedValue.fromString("")),
                        "Bank Name" to EntryValue.Plain("")
                    ))
                ),
                Entry(
                    uuid = java.util.UUID.randomUUID(),
                    icon = app.keemobile.kotpass.constants.PredefinedIcon.Note,
                    fields = EntryFields(mutableMapOf(
                        BasicField.Title() to EntryValue.Plain("Note"),
                        BasicField.UserName() to EntryValue.Plain(""),
                        BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString("")),
                        BasicField.Url() to EntryValue.Plain(""),
                        BasicField.Notes() to EntryValue.Plain("")
                    )),
                    customData = mapOf(
                        "TemplateType" to app.keemobile.kotpass.models.CustomDataValue("Note"), 
                        "ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Yellow"),
                        "Hide_UserName" to app.keemobile.kotpass.models.CustomDataValue("true"),
                        "Hide_Password" to app.keemobile.kotpass.models.CustomDataValue("true"),
                        "Hide_Url" to app.keemobile.kotpass.models.CustomDataValue("true")
                    )
                )
            )

            templatesGroup = app.keemobile.kotpass.models.Group(
                uuid = java.util.UUID.randomUUID(),
                name = "Templates",
                icon = app.keemobile.kotpass.constants.PredefinedIcon.Folder,
                entries = predefinedTemplates
            )
            
            withContext(Dispatchers.Default) {
                val updatedDb = db.modifyGroup(db.content.group.uuid) {
                    copy(groups = groups + templatesGroup!!)
                }
                withContext(Dispatchers.Main) {
                    _database.value = updatedDb
                    _hasUnsavedChanges.value = true
                }
            }
        }
        
        return templatesGroup
    }
    
    fun getTemplates(): List<Entry> {
        val db = _database.value ?: return emptyList()
        val templatesGroup = db.content.group.groups.find { it.name == "Templates" }
        return templatesGroup?.entries ?: emptyList()
    }
    
    fun deleteTemplate(entry: Entry) {
        viewModelScope.launch(Dispatchers.Default) {
            val db = _database.value ?: return@launch
            val templatesGroup = db.content.group.groups.find { it.name == "Templates" } ?: return@launch
            val updatedDb = db.modifyGroup(templatesGroup.uuid) {
                copy(entries = entries.filter { it.uuid != entry.uuid })
            }
            withContext(Dispatchers.Main) {
                _database.value = updatedDb
                _hasUnsavedChanges.value = true
            }
        }
    }
    
    fun addTemplate(title: String, username: String?, pass: String?, url: String?, notes: String?, iconName: String, color: String, customFields: List<com.example.ui.CustomFieldData>, tags: List<String> = emptyList()) {
        val icon = try { app.keemobile.kotpass.constants.PredefinedIcon.valueOf(iconName) } catch (e: Exception) { app.keemobile.kotpass.constants.PredefinedIcon.Key }
        val fieldsMap = mutableMapOf<String, EntryValue>()
        fieldsMap[BasicField.Title()] = EntryValue.Plain(title)
        if (username != null) fieldsMap[BasicField.UserName()] = EntryValue.Plain(username)
        if (pass != null) fieldsMap[BasicField.Password()] = EntryValue.Encrypted(EncryptedValue.fromString(pass))
        if (url != null) fieldsMap[BasicField.Url()] = EntryValue.Plain(url)
        if (notes != null) fieldsMap[BasicField.Notes()] = EntryValue.Plain(notes)
        
        for (field in customFields) {
            if (field.isHidden) {
                fieldsMap[field.name] = EntryValue.Encrypted(EncryptedValue.fromString(field.value))
            } else {
                fieldsMap[field.name] = EntryValue.Plain(field.value)
            }
        }
        val newEntry = Entry(
            uuid = java.util.UUID.randomUUID(),
            icon = icon,
            tags = tags,
            backgroundColor = color, foregroundColor = "#FFFFFF",
            customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue(color)) + customFields.associate { "ShowCopyButton_${it.name}" to app.keemobile.kotpass.models.CustomDataValue(it.showCopyButton.toString()) },
            fields = EntryFields(fieldsMap)
        )
        viewModelScope.launch(Dispatchers.Default) {
            val templatesGroup = getOrCreateTemplatesGroup()
            val updatedDb = _database.value!!.modifyGroup(templatesGroup.uuid) {
                copy(entries = entries + newEntry)
            }
            withContext(Dispatchers.Main) {
                _database.value = updatedDb
                _hasUnsavedChanges.value = true
            }
        }
    }
    
    fun createEntryFromTemplate(template: Entry) {
        viewModelScope.launch(Dispatchers.Default) {
            val db = _database.value ?: return@launch
            val currentGroup = _currentGroup.value ?: return@launch
            
            val newEntry = template.copy(uuid = java.util.UUID.randomUUID())
            val updatedDb = db.modifyGroup(currentGroup.uuid) {
                copy(entries = entries + newEntry)
            }
            withContext(Dispatchers.Main) {
                _database.value = updatedDb
                _hasUnsavedChanges.value = true
            }
        }
    }
    
    fun duplicateEntry(entry: Entry) {
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
    }

    fun duplicateGroup(group: app.keemobile.kotpass.models.Group) {
        val newGroup = group.copy(
            uuid = java.util.UUID.randomUUID(),
            name = group.name + " (Copy)"
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
    }

    fun deleteEntry(entry: Entry) {
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
    }

    fun deleteGroup(group: Group) {
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
    }

    fun saveDatabase() {
        realSaveDatabase()
    }

    fun realSaveDatabase() {
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
                    val newGroup = db.getGroup { it.uuid == currentGroupUuid }?.second ?: db.content.group
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
    }
    fun changeMasterPassword(newPass: String) {
        val db = _database.value ?: return
        val newCreds = app.keemobile.kotpass.database.Credentials.from(app.keemobile.kotpass.cryptography.EncryptedValue.fromString(newPass))
        val updatedDb = when (db) {
            is app.keemobile.kotpass.database.KeePassDatabase.Ver4x -> db.copy(credentials = newCreds)
            is app.keemobile.kotpass.database.KeePassDatabase.Ver3x -> db.copy(credentials = newCreds)
        }
        _database.value = updatedDb
        currentMasterPassword = newPass
        if (settings.enableBiometrics.value) {
            com.example.data.CryptoHelper.savePassword(context, newPass)
        }
        _hasUnsavedChanges.value = true
    }

    fun isRootGroup(): Boolean {
        return _currentGroup.value?.uuid == _database.value?.content?.group?.uuid
    }
    
    fun lockDatabase() {
        if (settings.clipboardAutoClear.value) {
            try {
                val clipboard = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.P) {
                    clipboard.clearPrimaryClip()
                } else {
                    clipboard.setPrimaryClip(android.content.ClipData.newPlainText("", ""))
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        currentMasterPassword = null
        _database.value = null
        _currentGroup.value = null
        _currentEntry.value = null
    }



    fun updateEntry(
        title: String,
        username: String?,
        pass: String?,
        url: String?,
        notes: String?,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>,
        tags: List<String> = emptyList()
    ) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return
        val entry = _currentEntry.value ?: return
        val parentUuid = findParentGroupUuidForEntry(currentDb.content.group, entry.uuid) ?: return

        val icon = try {
            app.keemobile.kotpass.constants.PredefinedIcon.valueOf(iconName)
        } catch (e: Exception) {
            app.keemobile.kotpass.constants.PredefinedIcon.Key
        }

        val fieldsMap = mutableMapOf<String, app.keemobile.kotpass.models.EntryValue>()
        fieldsMap[app.keemobile.kotpass.constants.BasicField.Title()] = app.keemobile.kotpass.models.EntryValue.Plain(title)
        if (username != null) fieldsMap[app.keemobile.kotpass.constants.BasicField.UserName()] = app.keemobile.kotpass.models.EntryValue.Plain(username)
        if (pass != null) fieldsMap[app.keemobile.kotpass.constants.BasicField.Password()] = app.keemobile.kotpass.models.EntryValue.Encrypted(app.keemobile.kotpass.cryptography.EncryptedValue.fromString(pass))
        if (url != null) fieldsMap[app.keemobile.kotpass.constants.BasicField.Url()] = app.keemobile.kotpass.models.EntryValue.Plain(url)
        if (notes != null) fieldsMap[app.keemobile.kotpass.constants.BasicField.Notes()] = app.keemobile.kotpass.models.EntryValue.Plain(notes)

        for (field in customFields) {
            if (field.isHidden) {
                fieldsMap[field.name] = app.keemobile.kotpass.models.EntryValue.Encrypted(app.keemobile.kotpass.cryptography.EncryptedValue.fromString(field.value))
            } else {
                fieldsMap[field.name] = app.keemobile.kotpass.models.EntryValue.Plain(field.value)
            }
        }

        val updatedEntry = entry.copy(
            icon = icon,
            tags = tags,
            backgroundColor = color, foregroundColor = "#FFFFFF",
            customData = entry.customData.toMutableMap().apply {
                put("ThemeColor", app.keemobile.kotpass.models.CustomDataValue(color))
                remove("Hide_UserName")
                remove("Hide_Password")
                remove("Hide_Url")
                remove("Hide_Notes")
            },
            fields = EntryFields(fieldsMap)
        )
        
        // Remove old entry and add new entry
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
        _hasUnsavedChanges.value = true
    }


    fun getAvailableGroupDestinationsForEntry(entry: Entry): List<GroupDestination> {
        val db = _database.value ?: return emptyList()
        val root = db.content.group
        val parentUuid = findParentGroupUuidForEntry(root, entry.uuid)
        val result = mutableListOf<GroupDestination>()

        fun traverse(g: Group, path: String, depth: Int) {
            val currentPath = if (path.isEmpty()) g.name else "$path / ${g.name}"
            result.add(
                GroupDestination(
                    group = g,
                    path = currentPath,
                    depth = depth,
                    isCurrentParent = (g.uuid == parentUuid),
                    isInvalid = (g.uuid == parentUuid)
                )
            )
            for (sub in g.groups) {
                traverse(sub, currentPath, depth + 1)
            }
        }

        traverse(root, "", 0)
        return result
    }

    fun getAvailableGroupDestinationsForGroup(groupToMove: Group): List<GroupDestination> {
        val db = _database.value ?: return emptyList()
        val root = db.content.group
        val parentUuid = findParentGroupUuidForGroup(root, groupToMove.uuid)
        val result = mutableListOf<GroupDestination>()

        fun isDescendant(parent: Group, targetUuid: UUID): Boolean {
            for (sub in parent.groups) {
                if (sub.uuid == targetUuid) return true
                if (isDescendant(sub, targetUuid)) return true
            }
            return false
        }

        fun traverse(g: Group, path: String, depth: Int) {
            val currentPath = if (path.isEmpty()) g.name else "$path / ${g.name}"
            val isSelf = g.uuid == groupToMove.uuid
            val isChild = isDescendant(groupToMove, g.uuid)
            val isParent = g.uuid == parentUuid
            val isInvalid = isSelf || isChild || isParent

            result.add(
                GroupDestination(
                    group = g,
                    path = currentPath,
                    depth = depth,
                    isCurrentParent = isParent,
                    isInvalid = isInvalid
                )
            )
            for (sub in g.groups) {
                traverse(sub, currentPath, depth + 1)
            }
        }

        traverse(root, "", 0)
        return result
    }

    fun moveEntry(entry: Entry, targetGroupUuid: UUID, onComplete: ((Boolean, String) -> Unit)? = null) {
        viewModelScope.launch(Dispatchers.Default) {
            val currentDb = _database.value ?: run {
                withContext(Dispatchers.Main) { onComplete?.invoke(false, "Database not available") }
                return@launch
            }
            val root = currentDb.content.group
            val sourceParentUuid = findParentGroupUuidForEntry(root, entry.uuid) ?: run {
                withContext(Dispatchers.Main) { onComplete?.invoke(false, "Source folder not found") }
                return@launch
            }
            if (sourceParentUuid == targetGroupUuid) {
                withContext(Dispatchers.Main) { onComplete?.invoke(true, "Already in this folder") }
                return@launch
            }
            val targetGroup = findGroupById(root, targetGroupUuid) ?: run {
                withContext(Dispatchers.Main) { onComplete?.invoke(false, "Destination folder not found") }
                return@launch
            }

            try {
                val dbWithoutEntry = currentDb.modifyGroup(sourceParentUuid) {
                    copy(entries = entries.filter { it.uuid != entry.uuid })
                }
                val finalDb = dbWithoutEntry.modifyGroup(targetGroupUuid) {
                    copy(entries = entries + entry)
                }

                withContext(Dispatchers.Main) {
                    _database.value = finalDb
                    val cg = _currentGroup.value
                    if (cg != null) {
                        _currentGroup.value = findGroupById(finalDb.content.group, cg.uuid) ?: finalDb.content.group
                    }
                    if (_currentEntry.value?.uuid == entry.uuid) {
                        _currentEntry.value = entry
                    }
                    if (_searchQuery.value.isNotEmpty()) {
                        setSearchQuery(_searchQuery.value)
                    }
                    _hasUnsavedChanges.value = true
                    onComplete?.invoke(true, "Moved to ${targetGroup.name}")
                }
            } catch (e: Exception) {
                e.printStackTrace()
                withContext(Dispatchers.Main) { onComplete?.invoke(false, e.localizedMessage ?: "Failed to move entry") }
            }
        }
    }

    fun moveGroup(group: Group, targetGroupUuid: UUID, onComplete: ((Boolean, String) -> Unit)? = null) {
        viewModelScope.launch(Dispatchers.Default) {
            val currentDb = _database.value ?: run {
                withContext(Dispatchers.Main) { onComplete?.invoke(false, "Database not available") }
                return@launch
            }
            val root = currentDb.content.group
            if (group.uuid == root.uuid) {
                withContext(Dispatchers.Main) { onComplete?.invoke(false, "Cannot move root folder") }
                return@launch
            }
            if (group.uuid == targetGroupUuid) {
                withContext(Dispatchers.Main) { onComplete?.invoke(false, "Cannot move folder into itself") }
                return@launch
            }
            if (findGroupById(group, targetGroupUuid) != null) {
                withContext(Dispatchers.Main) { onComplete?.invoke(false, "Cannot move folder into its own subfolder") }
                return@launch
            }
            val sourceParentUuid = findParentGroupUuidForGroup(root, group.uuid) ?: run {
                withContext(Dispatchers.Main) { onComplete?.invoke(false, "Source parent folder not found") }
                return@launch
            }
            if (sourceParentUuid == targetGroupUuid) {
                withContext(Dispatchers.Main) { onComplete?.invoke(true, "Already in this folder") }
                return@launch
            }
            val targetGroup = findGroupById(root, targetGroupUuid) ?: run {
                withContext(Dispatchers.Main) { onComplete?.invoke(false, "Destination folder not found") }
                return@launch
            }

            try {
                val dbWithoutGroup = currentDb.modifyGroup(sourceParentUuid) {
                    copy(groups = groups.filter { it.uuid != group.uuid })
                }
                val finalDb = dbWithoutGroup.modifyGroup(targetGroupUuid) {
                    copy(groups = groups + group)
                }

                withContext(Dispatchers.Main) {
                    _database.value = finalDb
                    val cg = _currentGroup.value
                    if (cg != null) {
                        _currentGroup.value = findGroupById(finalDb.content.group, cg.uuid) ?: finalDb.content.group
                    }
                    _hasUnsavedChanges.value = true
                    onComplete?.invoke(true, "Moved to ${targetGroup.name}")
                }
            } catch (e: Exception) {
                e.printStackTrace()
                withContext(Dispatchers.Main) { onComplete?.invoke(false, e.localizedMessage ?: "Failed to move folder") }
            }
        }
    }

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
}
