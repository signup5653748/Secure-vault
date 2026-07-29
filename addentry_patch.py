import re

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    content = f.read()

# Modify constructor
content = content.replace("fun AddEntryScreen(\n    viewModel: KeePassViewModel,\n    onNavigateBack: () -> Unit\n) {", 
"""fun AddEntryScreen(
    viewModel: KeePassViewModel,
    onNavigateBack: () -> Unit,
    isTemplate: Boolean = false
) {""")

# Modify save action
old_save = """                    onClick = {
                        viewModel.createEntry(
                            title = title,
                            username = username,
                            pass = password,
                            url = url,
                            notes = notes,
                            iconName = iconName,
                            color = color,
                            customFields = customFields
                        )
                        onNavigateBack()
                    },"""

new_save = """                    onClick = {
                        if (isTemplate) {
                            viewModel.addTemplate(
                                title = title,
                                username = username,
                                pass = password,
                                url = url,
                                notes = notes,
                                iconName = iconName,
                                color = color,
                                customFields = customFields
                            )
                        } else {
                            viewModel.createEntry(
                                title = title,
                                username = username,
                                pass = password,
                                url = url,
                                notes = notes,
                                iconName = iconName,
                                color = color,
                                customFields = customFields
                            )
                        }
                        onNavigateBack()
                    },"""

content = content.replace(old_save, new_save)

# Update title
content = content.replace('title = { Text("Add Entry") }', 'title = { Text(if (isTemplate) "Add Template" else "Add Entry") }')

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(content)
