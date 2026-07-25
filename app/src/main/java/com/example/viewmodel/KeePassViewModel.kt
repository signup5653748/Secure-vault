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
import app.keemobile.kotpass.models.Entry
import app.keemobile.kotpass.database.getGroup
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
