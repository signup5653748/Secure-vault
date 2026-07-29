import re

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    content = f.read()

imports = """import app.keemobile.kotpass.models.CustomDataValue
import app.keemobile.kotpass.constants.PredefinedIcon
import java.util.UUID
import app.keemobile.kotpass.database.modifiers.modifyGroup
import app.keemobile.kotpass.models.Entry
import app.keemobile.kotpass.models.EntryValue
import app.keemobile.kotpass.cryptography.EncryptedValue
import app.keemobile.kotpass.constants.BasicField
"""
content = content.replace("import app.keemobile.kotpass.models.Group", imports + "import app.keemobile.kotpass.models.Group")


funcs = """
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

        val updatedGroup = currentGroup.copy(
            groups = currentGroup.groups + newGroup
        )
        
        // This is a naive way, but modifying immutable database hierarchy is tricky.
        // We'll replace the current group in the database.
        val updatedDb = currentDb.modifyGroup(updatedGroup.uuid) { _ -> updatedGroup }
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

    fun createEntry(title: String, username: String, pass: String, url: String, notes: String) {
        val currentDb = _database.value ?: return
        val currentGroup = _currentGroup.value ?: return

        val newEntry = Entry(
            uuid = UUID.randomUUID(),
            fields = mapOf(
                BasicField.Title to EntryValue.Plain(title),
                BasicField.UserName to EntryValue.Plain(username),
                BasicField.Password to EntryValue.Encrypted(EncryptedValue.fromString(pass)),
                BasicField.URL to EntryValue.Plain(url),
                BasicField.Notes to EntryValue.Plain(notes)
            )
        )

        val updatedGroup = currentGroup.copy(
            entries = currentGroup.entries + newEntry
        )
        
        val updatedDb = currentDb.modifyGroup(updatedGroup.uuid) { _ -> updatedGroup }
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
"""

content = content.replace("    fun isRootGroup(): Boolean {", funcs + "\n    fun isRootGroup(): Boolean {")

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "w") as f:
    f.write(content)

