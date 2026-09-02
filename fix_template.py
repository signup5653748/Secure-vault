import re

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    text = f.read()

old_add = """    fun addTemplate(title: String, username: String, pass: String, url: String, notes: String, iconName: String, color: String, customFields: List<com.example.ui.CustomFieldData>, hiddenFields: List<String> = emptyList(), tags: List<String> = emptyList()) {
        val icon = try { app.keemobile.kotpass.constants.PredefinedIcon.valueOf(iconName) } catch (e: Exception) { app.keemobile.kotpass.constants.PredefinedIcon.Key }
        val fieldsMap = mutableMapOf<String, EntryValue>(
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
            uuid = java.util.UUID.randomUUID(),
            icon = icon,
            tags = tags,
            backgroundColor = color, foregroundColor = "#FFFFFF",
            customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue(color)) + customFields.associate { "ShowCopyButton_${it.name}" to app.keemobile.kotpass.models.CustomDataValue(it.showCopyButton.toString()) } + hiddenFields.associate { it to app.keemobile.kotpass.models.CustomDataValue("true") },
            fields = EntryFields(fieldsMap)
        )"""

new_add = """    fun addTemplate(title: String, username: String?, pass: String?, url: String?, notes: String?, iconName: String, color: String, customFields: List<com.example.ui.CustomFieldData>, tags: List<String> = emptyList()) {
        val icon = try { app.keemobile.kotpass.constants.PredefinedIcon.valueOf(iconName) } catch (e: Exception) { app.keemobile.kotpass.constants.PredefinedIcon.Key }
        val fieldsMap = mutableMapOf<String, EntryValue>()
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
            uuid = java.util.UUID.randomUUID(),
            icon = icon,
            tags = tags,
            backgroundColor = color, foregroundColor = "#FFFFFF",
            customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue(color)) + customFields.associate { "ShowCopyButton_${it.name}" to app.keemobile.kotpass.models.CustomDataValue(it.showCopyButton.toString()) },
            fields = EntryFields(fieldsMap)
        )"""
text = text.replace(old_add, new_add)
with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "w") as f:
    f.write(text)
