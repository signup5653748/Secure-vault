package com.example.viewmodel

import android.app.Application
import android.net.Uri
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.KeePassHelper
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import org.linguafranca.pwdb.Entry
import org.linguafranca.pwdb.Group
import org.linguafranca.pwdb.kdbx.dom.DomDatabaseWrapper
import java.io.File

class KeePassViewModel(application: Application) : AndroidViewModel(application) {

    private val context = application.applicationContext

    private val _dbFile = MutableStateFlow<File?>(null)
    val dbFile: StateFlow<File?> = _dbFile.asStateFlow()

    private val _database = MutableStateFlow<DomDatabaseWrapper?>(null)
    val database: StateFlow<DomDatabaseWrapper?> = _database.asStateFlow()

    private val _currentGroup = MutableStateFlow<Group<*, *, *, *>?>(null)
    val currentGroup: StateFlow<Group<*, *, *, *>?> = _currentGroup.asStateFlow()

    private val _currentEntry = MutableStateFlow<Entry<*, *, *, *>?>(null)
    val currentEntry: StateFlow<Entry<*, *, *, *>?> = _currentEntry.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    init {
        checkExistingFile()
    }

    private fun checkExistingFile() {
        val file = File(context.filesDir, "keepass.kdbx")
        if (file.exists()) {
            _dbFile.value = file
        }
    }

    fun importFile(uri: Uri) {
        viewModelScope.launch {
            val file = KeePassHelper.copyToInternalStorage(context, uri)
            if (file != null) {
                _dbFile.value = file
                _error.value = null
            } else {
                _error.value = "Failed to copy file"
            }
        }
    }

    fun unlockDatabase(password: String) {
        viewModelScope.launch {
            val file = _dbFile.value
            if (file != null) {
                val db = KeePassHelper.loadDatabase(file, password)
                if (db != null) {
                    _database.value = db
                    _currentGroup.value = db.rootGroup
                    _error.value = null
                } else {
                    _error.value = "Failed to unlock database. Incorrect password or invalid file."
                }
            }
        }
    }

    fun selectGroup(group: Group<*, *, *, *>) {
        _currentGroup.value = group
    }

    fun navigateUp() {
        val parent = _currentGroup.value?.parent
        if (parent != null) {
            _currentGroup.value = parent
        }
    }

    fun selectEntry(entry: Entry<*, *, *, *>) {
        _currentEntry.value = entry
    }

    fun clearError() {
        _error.value = null
    }
    
    fun lockDatabase() {
        _database.value = null
        _currentGroup.value = null
        _currentEntry.value = null
    }
}
