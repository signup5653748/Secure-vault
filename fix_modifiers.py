import re

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    content = f.read()

# Fix createGroup
content = content.replace("""        val updatedGroup = currentGroup.copy(
            groups = currentGroup.groups + newGroup
        )
        
        // This is a naive way, but modifying immutable database hierarchy is tricky.
        // We'll replace the current group in the database.
        val updatedDb = currentDb.modifyGroup(updatedGroup.uuid) { _ -> updatedGroup }""", """        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(groups = groups + newGroup)
        }""")

# Fix createEntry
content = content.replace("""        val updatedGroup = currentGroup.copy(
            entries = currentGroup.entries + newEntry
        )
        
        val updatedDb = currentDb.modifyGroup(updatedGroup.uuid) { _ -> updatedGroup }""", """        val updatedDb = currentDb.modifyGroup(currentGroup.uuid) {
            copy(entries = entries + newEntry)
        }""")

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "w") as f:
    f.write(content)

