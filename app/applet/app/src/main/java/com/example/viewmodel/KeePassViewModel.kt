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

    fun importFile(uri: Uri) {
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

    private fun findParentGroup(root: Group, childUuid: java.util.UUID): Group? {
        if (root.groups.any { it.uuid == childUuid }) return root
        for (g in root.groups) {
            val p = findParentGroup(g, childUuid)
            if (p != null) return p
        }
        return null
    }

    fun navigateUp() {
        val currentGroupUuid = _currentGroup.value?.uuid ?: return
        val rootGroup = _database.value?.content?.group ?: return
        val parent = findParentGroup(rootGroup, currentGroupUuid)
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
        val newCurrentGroup = updatedDb.getGroup { it.uuid == currentGroup.uuid }?.first
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
        customFields: List<Triple<String, String, Boolean>>
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
            if (field.third) {
                fieldsMap[field.first] = EntryValue.Encrypted(EncryptedValue.fromString(field.second))
            } else {
                fieldsMap[field.first] = EntryValue.Plain(field.second)
            }
        }

        val newEntry = Entry(
            uuid = UUID.randomUUID(),
            icon = icon,
            customData = mapOf("ThemeColor" to CustomDataValue(color)),
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
        
        val newCurrentGroup = updatedDb.getGroup { it.uuid == currentGroup.uuid }?.first
        if (newCurrentGroup != null) {
            _currentGroup.value = newCurrentGroup
        }
    }

    fun isRootGroup(): Boolean {
        return _currentGroup.value?.uuid == _database.value?.content?.group?.uuid
    }
    
    fun lockDatabase() {
        _database.value = null
        _currentGroup.value = null
        _currentEntry.value = null
        _dbUri.value = null
        settings.setDatabaseUri(null)
    }
}
