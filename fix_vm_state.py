import sys

with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

target_db = """    private val _database = MutableStateFlow<KeePassDatabase?>(null)
    val database: StateFlow<KeePassDatabase?> = _database.asStateFlow()"""

replacement_db = """    private val _database = MutableStateFlow<KeePassDatabase?>(null)
    val database: StateFlow<KeePassDatabase?> = _database.asStateFlow()

    private val _hasUnsavedChanges = MutableStateFlow(false)
    val hasUnsavedChanges: StateFlow<Boolean> = _hasUnsavedChanges.asStateFlow()"""

content = content.replace(target_db, replacement_db)

with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
print("Added hasUnsavedChanges state")
