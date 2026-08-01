with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    text = f.read()

functions_to_add = """
    private fun findParentGroupUuidForEntry(group: app.keemobile.kotpass.models.Group, entryUuid: java.util.UUID): java.util.UUID? {
        if (group.entries.any { it.uuid == entryUuid }) return group.uuid
        for (sub in group.groups) {
            val res = findParentGroupUuidForEntry(sub, entryUuid)
            if (res != null) return res
        }
        return null
    }

    private fun findParentGroupUuidForGroup(group: app.keemobile.kotpass.models.Group, groupUuid: java.util.UUID): java.util.UUID? {
        if (group.groups.any { it.uuid == groupUuid }) return group.uuid
        for (sub in group.groups) {
            val res = findParentGroupUuidForGroup(sub, groupUuid)
            if (res != null) return res
        }
        return null
    }
    
    private fun findGroupById(group: app.keemobile.kotpass.models.Group, uuid: java.util.UUID): app.keemobile.kotpass.models.Group? {
        if (group.uuid == uuid) return group
        for (sub in group.groups) {
            val res = findGroupById(sub, uuid)
            if (res != null) return res
        }
        return null
    }
}
"""

text = text.rstrip()
if text.endswith("}"):
    text = text[:-1] + functions_to_add

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "w") as f:
    f.write(text)

