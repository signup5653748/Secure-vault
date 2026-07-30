import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

# createEntry
create_old = """    fun createEntry(
        title: String,
        username: String,
        pass: String,
        url: String,
        notes: String,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>
    ) {"""
create_new = """    fun createEntry(
        title: String,
        username: String,
        pass: String,
        url: String,
        notes: String,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>,
        hiddenFields: List<String> = emptyList()
    ) {"""
content = content.replace(create_old, create_new)

create_custom_data_old = """            customData = mapOf("ThemeColor" to CustomDataValue(color)) + customFields.associate { "ShowCopyButton_${it.name}" to CustomDataValue(it.showCopyButton.toString()) },"""
create_custom_data_new = """            customData = mapOf("ThemeColor" to CustomDataValue(color)) + customFields.associate { "ShowCopyButton_${it.name}" to CustomDataValue(it.showCopyButton.toString()) } + hiddenFields.associate { it to CustomDataValue("true") },"""
content = content.replace(create_custom_data_old, create_custom_data_new)

# addTemplate
add_old = """    fun addTemplate(
        title: String,
        username: String,
        pass: String,
        url: String,
        notes: String,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>
    ) {"""
add_new = """    fun addTemplate(
        title: String,
        username: String,
        pass: String,
        url: String,
        notes: String,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>,
        hiddenFields: List<String> = emptyList()
    ) {"""
content = content.replace(add_old, add_new)

add_custom_data_old = """            customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue(color)) + customFields.associate { "ShowCopyButton_${it.name}" to app.keemobile.kotpass.models.CustomDataValue(it.showCopyButton.toString()) },"""
add_custom_data_new = """            customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue(color)) + customFields.associate { "ShowCopyButton_${it.name}" to app.keemobile.kotpass.models.CustomDataValue(it.showCopyButton.toString()) } + hiddenFields.associate { it to app.keemobile.kotpass.models.CustomDataValue("true") },"""
content = content.replace(add_custom_data_old, add_custom_data_new)

# updateEntry
update_old = """    fun updateEntry(
        title: String,
        username: String,
        pass: String,
        url: String,
        notes: String,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>
    ) {"""
update_new = """    fun updateEntry(
        title: String,
        username: String,
        pass: String,
        url: String,
        notes: String,
        iconName: String,
        color: String,
        customFields: List<com.example.ui.CustomFieldData>,
        hiddenFields: List<String> = emptyList()
    ) {"""
content = content.replace(update_old, update_new)

update_custom_data_old = """        val updatedEntry = entry.copy(
            icon = icon,
            customData = entry.customData.toMutableMap().apply {
                put("ThemeColor", app.keemobile.kotpass.models.CustomDataValue(color))
            },"""
update_custom_data_new = """        val updatedEntry = entry.copy(
            icon = icon,
            customData = entry.customData.toMutableMap().apply {
                put("ThemeColor", app.keemobile.kotpass.models.CustomDataValue(color))
                remove("Hide_UserName")
                remove("Hide_Password")
                remove("Hide_Url")
                remove("Hide_Notes")
                hiddenFields.forEach { put(it, app.keemobile.kotpass.models.CustomDataValue("true")) }
            },"""
content = content.replace(update_custom_data_old, update_custom_data_new)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
