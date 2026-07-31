import sys

with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

target = """    fun isRootGroup(): Boolean {"""

replacement = """    fun changeMasterPassword(newPass: String) {
        val db = _database.value ?: return
        val newCreds = app.keemobile.kotpass.database.Credentials.from(app.keemobile.kotpass.cryptography.EncryptedValue.fromString(newPass))
        val updatedDb = when (db) {
            is app.keemobile.kotpass.database.KeePassDatabase.Ver4x -> db.copy(credentials = newCreds)
            is app.keemobile.kotpass.database.KeePassDatabase.Ver3x -> db.copy(credentials = newCreds)
        }
        _database.value = updatedDb
        _hasUnsavedChanges.value = true
        saveDatabase() // Auto-save when password changes? The prompt says "re-encrypt the currently opened KDBX database". We can call realSaveDatabase(). Wait, let's auto-save to make it permanent immediately.
    }

    fun isRootGroup(): Boolean {"""

content = content.replace(target, replacement)

with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
print("Added changeMasterPassword")
