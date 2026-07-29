import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

add_template_old = """        val newEntry = Entry(
            uuid = java.util.UUID.randomUUID(),
            icon = icon,
            customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue(color)),
            fields = EntryFields(fieldsMap)
        )"""

add_template_new = """        val newEntry = Entry(
            uuid = java.util.UUID.randomUUID(),
            icon = icon,
            customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue(color)) + customFields.associate { "ShowCopyButton_${it.name}" to app.keemobile.kotpass.models.CustomDataValue(it.showCopyButton.toString()) },
            fields = EntryFields(fieldsMap)
        )"""

content = content.replace(add_template_old, add_template_new)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
