import re

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    content = f.read()

# Fix updateGroup
content = content.replace(
    "val newCurrentGroup = if (updatedDb.content.group.uuid == currentGroup.uuid) updatedDb.content.group else updatedDb.getGroup { it.uuid == currentGroup.uuid }?.first",
    "val newCurrentGroup = if (updatedDb.content.group.uuid == currentGroup.uuid) updatedDb.content.group else updatedDb.getGroup { it.uuid == currentGroup.uuid }?.second"
)

# Fix duplicateEntry
content = content.replace(
    "_currentGroup.value = updatedDb.getGroup { it.uuid == currentGroupUuid }?.first ?: _currentGroup.value",
    "_currentGroup.value = updatedDb.getGroup { it.uuid == currentGroupUuid }?.second ?: _currentGroup.value"
)

# Fix deleteEntry
content = content.replace(
    "val newGroup = db.getGroup { it.uuid == currentGroupUuid }?.first ?: db.content.group",
    "val newGroup = db.getGroup { it.uuid == currentGroupUuid }?.second ?: db.content.group"
)

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "w") as f:
    f.write(content)
print("fixed")
