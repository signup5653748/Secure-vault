import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

# Replace:
# val mappedFields = customFields.map { Triple(it.name, it.value, it.isHidden) }
# if (isTemplate) {
#     viewModel.addTemplate(title, username, password, url, notes, iconName, color, mappedFields)
# } else {
#     viewModel.createEntry(title, username, password, url, notes, iconName, color, mappedFields)
# }

old_block = """                    val mappedFields = customFields.map { Triple(it.name, it.value, it.isHidden) }
                    if (isTemplate) {
                        viewModel.addTemplate(title, username, password, url, notes, iconName, color, mappedFields)
                    } else {
                        viewModel.createEntry(title, username, password, url, notes, iconName, color, mappedFields)
                    }"""

new_block = """                    if (isTemplate) {
                        viewModel.addTemplate(title, username, password, url, notes, iconName, color, customFields)
                    } else {
                        viewModel.createEntry(title, username, password, url, notes, iconName, color, customFields)
                    }"""

content = content.replace(old_block, new_block)

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)

