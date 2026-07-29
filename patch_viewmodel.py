import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

# Add _isLoading
state_old = """    private val _dbUri = MutableStateFlow<Uri?>(null)
    val dbUri: StateFlow<Uri?> = _dbUri"""
state_new = """    private val _dbUri = MutableStateFlow<Uri?>(null)
    val dbUri: StateFlow<Uri?> = _dbUri
    
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading"""
content = content.replace(state_old, state_new)

# Update unlockDatabase
unlock_old = """    fun unlockDatabase(password: String) {
        viewModelScope.launch {
            val uri = _dbUri.value
            if (uri != null) {
                try {
                    val db = KeePassHelper.loadDatabase(context, uri, password)"""
unlock_new = """    fun unlockDatabase(password: String) {
        viewModelScope.launch {
            _isLoading.value = true
            val uri = _dbUri.value
            if (uri != null) {
                try {
                    val db = KeePassHelper.loadDatabase(context, uri, password)"""
content = content.replace(unlock_old, unlock_new)

# Update unlockDatabase catch
unlock_catch_old = """                    } else {
                        _error.value = "Failed to unlock database. Incorrect password or invalid file."
                    }
                } catch (e: Exception) {
                    _error.value = "Error: ${e.message}"
                }
            } else {
                _error.value = "No database file selected."
            }
        }
    }"""
unlock_catch_new = """                    } else {
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
    }"""
content = content.replace(unlock_catch_old, unlock_catch_new)

# Add to createDatabase
create_old = """    fun createDatabase(uri: Uri, password: String) {
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val db = KeePassHelper.createDatabase(password)"""
create_new = """    fun createDatabase(uri: Uri, password: String) {
        viewModelScope.launch(Dispatchers.IO) {
            _isLoading.value = true
            try {
                val db = KeePassHelper.createDatabase(password)"""
content = content.replace(create_old, create_new)

create_catch_old = """            } catch (e: Exception) {
                _error.value = "Error creating database: ${e.message}"
            }
        }
    }"""
create_catch_new = """            } catch (e: Exception) {
                _error.value = "Error creating database: ${e.message}"
            } finally {
                _isLoading.value = false
            }
        }
    }"""
content = content.replace(create_catch_old, create_catch_new)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
