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

class KeePassViewModel(application: Application) : AndroidViewModel(application) {

    private val context = application.applicationContext
    val settings = SettingsRepository(context)

    private val _dbUri = MutableStateFlow<Uri?>(null)
    val dbUri: StateFlow<Uri?> = _dbUri.asStateFlow()

    private val _database = MutableStateFlow<KeePassDatabase?>(null)
    val database: StateFlow<KeePassDatabase?> = _database.asStateFlow()

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
            val uri = _dbUri.value
            if (uri != null) {
                try {
                    val db = KeePassHelper.loadDatabase(context, uri, password)
                    if (db != null) {
                        _database.value = db
                        _currentGroup.value = db.content.group
                        _error.value = null
                    } else {
                        _error.value = "Failed to unlock database. Incorrect password or invalid file."
                    }
                } catch (e: Exception) {
                    _error.value = "Error: ${e.message}"
                }
            } else {
                _error.value = "No database file selected."
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

    fun selectEntry(entry: Entry) {
        _currentEntry.value = entry
    }

    fun clearError() {
        _error.value = null
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
        
        // Update current group to trigger recompose
        val newCurrentGroup = if (updatedDb.content.group.uuid == currentGroup.uuid) updatedDb.content.group else updatedDb.getGroup { it.uuid == currentGroup.uuid }?.first
        if (newCurrentGroup != null) {
            _currentGroup.value = newCurrentGroup
        }
    }

    fun createEntry(
        title: String,
        username: String,
        pass: String,
        url: String,
        notes: String,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>
    ) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return
        
        val icon = try {
            PredefinedIcon.valueOf(iconName)
        } catch (e: Exception) {
            PredefinedIcon.Key
        }
        
        val fieldsMap = mutableMapOf<String, EntryValue>(
            BasicField.Title() to EntryValue.Plain(title),
            BasicField.UserName() to EntryValue.Plain(username),
            BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString(pass)),
            BasicField.Url() to EntryValue.Plain(url),
            BasicField.Notes() to EntryValue.Plain(notes)
        )
        
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
            customData = mapOf("ThemeColor" to CustomDataValue(color)) + customFields.associate { "ShowCopyButton_${it.name}" to CustomDataValue(it.showCopyButton.toString()) },
            fields = EntryFields(fieldsMap)
        )
        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
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
                    customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Green")),
                    fields = EntryFields(mutableMapOf(
                        BasicField.Title() to EntryValue.Plain("Bank Account"),
                        BasicField.UserName() to EntryValue.Plain(""),
                        BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString("")),
                        BasicField.Url() to EntryValue.Plain("")
                    ))
                ),
                Entry(
                    uuid = java.util.UUID.randomUUID(),
                    icon = app.keemobile.kotpass.constants.PredefinedIcon.Note,
                    fields = EntryFields(mutableMapOf(
                        BasicField.Title() to EntryValue.Plain("Note"),
                        BasicField.Notes() to EntryValue.Plain("")
                    )),
                    customData = mapOf("TemplateType" to app.keemobile.kotpass.models.CustomDataValue("Note"), "ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Yellow"))
                )
            )

            templatesGroup = app.keemobile.kotpass.models.Group(
                uuid = java.util.UUID.randomUUID(),
                name = "Templates",
                icon = app.keemobile.kotpass.constants.PredefinedIcon.Folder,
                entries = predefinedTemplates
            )
            
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
    
    fun addTemplate(title: String, username: String, pass: String, url: String, notes: String, iconName: String, color: String, customFields: List<com.example.ui.CustomFieldData>) {
        val icon = try { app.keemobile.kotpass.constants.PredefinedIcon.valueOf(iconName) } catch (e: Exception) { app.keemobile.kotpass.constants.PredefinedIcon.Key }
        val fieldsMap = mutableMapOf<String, EntryValue>(
            BasicField.Title() to EntryValue.Plain(title),
            BasicField.UserName() to EntryValue.Plain(username),
            BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString(pass)),
            BasicField.Url() to EntryValue.Plain(url),
            BasicField.Notes() to EntryValue.Plain(notes)
        )
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
    
    fun deleteEntry(entry: Entry) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return
        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(entries = entries.filter { it.uuid != entry.uuid })
        }
        _database.value = updatedDb
        saveDatabase()
    }

    fun deleteGroup(group: Group) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return
        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(groups = groups.filter { it.uuid != group.uuid })
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
        _database.value = null
        _currentGroup.value = null
        _currentEntry.value = null
    }
}
