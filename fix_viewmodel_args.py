import re

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    text = f.read()

# For createEntry:
old_create = """    fun createEntry(
        title: String,
        username: String,
        pass: String,
        url: String,
        notes: String,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>,
        hiddenFields: List<String> = emptyList(),
        tags: List<String> = emptyList()
    ) {"""

new_create = """    fun createEntry(
        title: String,
        username: String?,
        pass: String?,
        url: String?,
        notes: String?,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>,
        tags: List<String> = emptyList()
    ) {"""
text = text.replace(old_create, new_create)

old_create_map = """        val fieldsMap = mutableMapOf<String, EntryValue>(
            BasicField.Title() to EntryValue.Plain(title),
            BasicField.UserName() to EntryValue.Plain(username),
            BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString(pass)),
            BasicField.Url() to EntryValue.Plain(url),
            BasicField.Notes() to EntryValue.Plain(notes)
        )
        
        for (field in customFields) {
            if (field.isHidden) {
                fieldsMap[field.name] = EntryValue.Encrypted(EncryptedValue.fromString(field.value))
            } else {
                fieldsMap[field.name] = EntryValue.Plain(field.value)
            }
        }

        val newEntry = Entry(
            uuid = UUID.randomUUID(),
            icon = icon,
            tags = tags,
            backgroundColor = color, foregroundColor = "#FFFFFF",
            customData = mapOf("ThemeColor" to CustomDataValue(color)) + customFields.associate { "ShowCopyButton_${it.name}" to CustomDataValue(it.showCopyButton.toString()) } + hiddenFields.associate { it to CustomDataValue("true") },
            fields = EntryFields(fieldsMap)
        )"""

new_create_map = """        val fieldsMap = mutableMapOf<String, EntryValue>()
        fieldsMap[BasicField.Title()] = EntryValue.Plain(title)
        if (username != null) fieldsMap[BasicField.UserName()] = EntryValue.Plain(username)
        if (pass != null) fieldsMap[BasicField.Password()] = EntryValue.Encrypted(EncryptedValue.fromString(pass))
        if (url != null) fieldsMap[BasicField.Url()] = EntryValue.Plain(url)
        if (notes != null) fieldsMap[BasicField.Notes()] = EntryValue.Plain(notes)
        
        for (field in customFields) {
            if (field.isHidden) {
                fieldsMap[field.name] = EntryValue.Encrypted(EncryptedValue.fromString(field.value))
            } else {
                fieldsMap[field.name] = EntryValue.Plain(field.value)
            }
        }

        val newEntry = Entry(
            uuid = UUID.randomUUID(),
            icon = icon,
            tags = tags,
            backgroundColor = color, foregroundColor = "#FFFFFF",
            customData = mapOf("ThemeColor" to CustomDataValue(color)) + customFields.associate { "ShowCopyButton_${it.name}" to CustomDataValue(it.showCopyButton.toString()) },
            fields = EntryFields(fieldsMap)
        )"""
text = text.replace(old_create_map, new_create_map)

# For addTemplate:
old_template = """    fun addTemplate(
        title: String,
        username: String,
        pass: String,
        url: String,
        notes: String,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>,
        hiddenFields: List<String> = emptyList(),
        tags: List<String> = emptyList()
    ) {"""

new_template = """    fun addTemplate(
        title: String,
        username: String?,
        pass: String?,
        url: String?,
        notes: String?,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>,
        tags: List<String> = emptyList()
    ) {"""
text = text.replace(old_template, new_template)

old_template_map = """        val fieldsMap = mutableMapOf<String, app.keemobile.kotpass.models.EntryValue>(
            app.keemobile.kotpass.constants.BasicField.Title() to app.keemobile.kotpass.models.EntryValue.Plain(title),
            app.keemobile.kotpass.constants.BasicField.UserName() to app.keemobile.kotpass.models.EntryValue.Plain(username),
            app.keemobile.kotpass.constants.BasicField.Password() to app.keemobile.kotpass.models.EntryValue.Encrypted(app.keemobile.kotpass.cryptography.EncryptedValue.fromString(pass)),
            app.keemobile.kotpass.constants.BasicField.Url() to app.keemobile.kotpass.models.EntryValue.Plain(url),
            app.keemobile.kotpass.constants.BasicField.Notes() to app.keemobile.kotpass.models.EntryValue.Plain(notes)
        )
        for (field in customFields) {
            if (field.isHidden) {
                fieldsMap[field.name] = app.keemobile.kotpass.models.EntryValue.Encrypted(app.keemobile.kotpass.cryptography.EncryptedValue.fromString(field.value))
            } else {
                fieldsMap[field.name] = app.keemobile.kotpass.models.EntryValue.Plain(field.value)
            }
        }
        val newEntry = Entry(
            uuid = java.util.UUID.randomUUID(),
            icon = icon,
            tags = tags,
            backgroundColor = color, foregroundColor = "#FFFFFF",
            customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue(color)) + customFields.associate { "ShowCopyButton_${it.name}" to app.keemobile.kotpass.models.CustomDataValue(it.showCopyButton.toString()) } + hiddenFields.associate { it to app.keemobile.kotpass.models.CustomDataValue("true") },
            fields = EntryFields(fieldsMap)
        )"""

new_template_map = """        val fieldsMap = mutableMapOf<String, app.keemobile.kotpass.models.EntryValue>()
        fieldsMap[app.keemobile.kotpass.constants.BasicField.Title()] = app.keemobile.kotpass.models.EntryValue.Plain(title)
        if (username != null) fieldsMap[app.keemobile.kotpass.constants.BasicField.UserName()] = app.keemobile.kotpass.models.EntryValue.Plain(username)
        if (pass != null) fieldsMap[app.keemobile.kotpass.constants.BasicField.Password()] = app.keemobile.kotpass.models.EntryValue.Encrypted(app.keemobile.kotpass.cryptography.EncryptedValue.fromString(pass))
        if (url != null) fieldsMap[app.keemobile.kotpass.constants.BasicField.Url()] = app.keemobile.kotpass.models.EntryValue.Plain(url)
        if (notes != null) fieldsMap[app.keemobile.kotpass.constants.BasicField.Notes()] = app.keemobile.kotpass.models.EntryValue.Plain(notes)
        
        for (field in customFields) {
            if (field.isHidden) {
                fieldsMap[field.name] = app.keemobile.kotpass.models.EntryValue.Encrypted(app.keemobile.kotpass.cryptography.EncryptedValue.fromString(field.value))
            } else {
                fieldsMap[field.name] = app.keemobile.kotpass.models.EntryValue.Plain(field.value)
            }
        }
        val newEntry = Entry(
            uuid = java.util.UUID.randomUUID(),
            icon = icon,
            tags = tags,
            backgroundColor = color, foregroundColor = "#FFFFFF",
            customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue(color)) + customFields.associate { "ShowCopyButton_${it.name}" to app.keemobile.kotpass.models.CustomDataValue(it.showCopyButton.toString()) },
            fields = EntryFields(fieldsMap)
        )"""
text = text.replace(old_template_map, new_template_map)

# For updateEntry:
old_update = """    fun updateEntry(
        title: String,
        username: String,
        pass: String,
        url: String,
        notes: String,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>,
        hiddenFields: List<String> = emptyList(),
        tags: List<String> = emptyList()
    ) {"""

new_update = """    fun updateEntry(
        title: String,
        username: String?,
        pass: String?,
        url: String?,
        notes: String?,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>,
        tags: List<String> = emptyList()
    ) {"""
text = text.replace(old_update, new_update)

old_update_map = """        val fieldsMap = mutableMapOf<String, app.keemobile.kotpass.models.EntryValue>(
            app.keemobile.kotpass.constants.BasicField.Title() to app.keemobile.kotpass.models.EntryValue.Plain(title),
            app.keemobile.kotpass.constants.BasicField.UserName() to app.keemobile.kotpass.models.EntryValue.Plain(username),
            app.keemobile.kotpass.constants.BasicField.Password() to app.keemobile.kotpass.models.EntryValue.Encrypted(app.keemobile.kotpass.cryptography.EncryptedValue.fromString(pass)),
            app.keemobile.kotpass.constants.BasicField.Url() to app.keemobile.kotpass.models.EntryValue.Plain(url),
            app.keemobile.kotpass.constants.BasicField.Notes() to app.keemobile.kotpass.models.EntryValue.Plain(notes)
        )

        for (field in customFields) {
            if (field.isHidden) {
                fieldsMap[field.name] = app.keemobile.kotpass.models.EntryValue.Encrypted(app.keemobile.kotpass.cryptography.EncryptedValue.fromString(field.value))
            } else {
                fieldsMap[field.name] = app.keemobile.kotpass.models.EntryValue.Plain(field.value)
            }
        }

        val updatedEntry = entry.copy(
            icon = icon,
            tags = tags,
            backgroundColor = color, foregroundColor = "#FFFFFF",
            customData = entry.customData.toMutableMap().apply {
                put("ThemeColor", app.keemobile.kotpass.models.CustomDataValue(color))
                remove("Hide_UserName")
                remove("Hide_Password")
                remove("Hide_Url")
                remove("Hide_Notes")
                hiddenFields.forEach { put(it, app.keemobile.kotpass.models.CustomDataValue("true")) }
            },
            fields = EntryFields(fieldsMap)
        )"""

new_update_map = """        val fieldsMap = mutableMapOf<String, app.keemobile.kotpass.models.EntryValue>()
        fieldsMap[app.keemobile.kotpass.constants.BasicField.Title()] = app.keemobile.kotpass.models.EntryValue.Plain(title)
        if (username != null) fieldsMap[app.keemobile.kotpass.constants.BasicField.UserName()] = app.keemobile.kotpass.models.EntryValue.Plain(username)
        if (pass != null) fieldsMap[app.keemobile.kotpass.constants.BasicField.Password()] = app.keemobile.kotpass.models.EntryValue.Encrypted(app.keemobile.kotpass.cryptography.EncryptedValue.fromString(pass))
        if (url != null) fieldsMap[app.keemobile.kotpass.constants.BasicField.Url()] = app.keemobile.kotpass.models.EntryValue.Plain(url)
        if (notes != null) fieldsMap[app.keemobile.kotpass.constants.BasicField.Notes()] = app.keemobile.kotpass.models.EntryValue.Plain(notes)

        for (field in customFields) {
            if (field.isHidden) {
                fieldsMap[field.name] = app.keemobile.kotpass.models.EntryValue.Encrypted(app.keemobile.kotpass.cryptography.EncryptedValue.fromString(field.value))
            } else {
                fieldsMap[field.name] = app.keemobile.kotpass.models.EntryValue.Plain(field.value)
            }
        }

        val updatedEntry = entry.copy(
            icon = icon,
            tags = tags,
            backgroundColor = color, foregroundColor = "#FFFFFF",
            customData = entry.customData.toMutableMap().apply {
                put("ThemeColor", app.keemobile.kotpass.models.CustomDataValue(color))
                remove("Hide_UserName")
                remove("Hide_Password")
                remove("Hide_Url")
                remove("Hide_Notes")
            },
            fields = EntryFields(fieldsMap)
        )"""
text = text.replace(old_update_map, new_update_map)

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "w") as f:
    f.write(text)
