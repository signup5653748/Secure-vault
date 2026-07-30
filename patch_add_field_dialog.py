import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

old_add = """                    TextButton(onClick = {
                        if (fieldName.isNotBlank()) {
                            customFields = customFields + CustomFieldData(name = fieldName, value = fieldValue, isHidden = isHidden, showCopyButton = showCopyButton)
                        }
                        showAddFieldDialog = false
                    }) { Text("Add") }"""

new_add = """                    TextButton(onClick = {
                        if (fieldName.equals("Username", ignoreCase = true) && !showUsername) {
                            showUsername = true
                            username = fieldValue
                        } else if (fieldName.equals("Password", ignoreCase = true) && !showPassword) {
                            showPassword = true
                            password = fieldValue
                        } else if (fieldName.equals("URL", ignoreCase = true) && !showUrl) {
                            showUrl = true
                            url = fieldValue
                        } else if (fieldName.equals("Notes", ignoreCase = true) && !showNotes) {
                            showNotes = true
                            notes = fieldValue
                        } else if (fieldName.isNotBlank()) {
                            customFields = customFields + CustomFieldData(name = fieldName, value = fieldValue, isHidden = isHidden, showCopyButton = showCopyButton)
                        }
                        showAddFieldDialog = false
                    }) { Text("Add") }"""

content = content.replace(old_add, new_add)

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)
