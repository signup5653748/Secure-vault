import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

args_old = """fun AddEntryScreen(
    viewModel: KeePassViewModel,
    onNavigateBack: () -> Unit,
    isTemplate: Boolean = false
) {"""
args_new = """fun AddEntryScreen(
    viewModel: KeePassViewModel,
    onNavigateBack: () -> Unit,
    isTemplate: Boolean = false,
    isEdit: Boolean = false
) {
    val currentEntry by viewModel.currentEntry.collectAsState()"""
content = content.replace(args_old, args_new)

vars_old = """    var title by remember { mutableStateOf("") }
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var url by remember { mutableStateOf("") }
    var notes by remember { mutableStateOf("") }
    var iconName by remember { mutableStateOf("Key") }
    var color by remember { mutableStateOf("Blue") }
    
    var customFields by remember { mutableStateOf(listOf<CustomFieldData>()) }"""
vars_new = """    var title by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!![app.keemobile.kotpass.constants.BasicField.Title]?.content ?: "" else "") }
    var username by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!![app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: "" else "") }
    var password by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!![app.keemobile.kotpass.constants.BasicField.Password]?.content ?: "" else "") }
    var url by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!![app.keemobile.kotpass.constants.BasicField.Url]?.content ?: "" else "") }
    var notes by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!![app.keemobile.kotpass.constants.BasicField.Notes]?.content ?: "" else "") }
    var iconName by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.icon.name else "Key") }
    var color by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["ThemeColor"]?.value ?: "Blue" else "Blue") }
    
    var customFields by remember { mutableStateOf(
        if (isEdit && currentEntry != null) {
            val basicKeys = setOf("Title", "UserName", "Password", "URL", "Notes")
            currentEntry!!.fields.entries.filter { it.key !in basicKeys }.map {
                CustomFieldData(it.key, it.value.content, it.value is app.keemobile.kotpass.models.EntryValue.Encrypted)
            }
        } else listOf<CustomFieldData>()
    ) }"""
content = content.replace(vars_old, vars_new)

btn_old = """                IconButton(onClick = {
                    if (!isSaving) {
                        isSaving = true
                        if (isTemplate) {
                            viewModel.addTemplate(title, username, password, url, notes, iconName, color, customFields)
                        } else {
                            viewModel.createEntry(title, username, password, url, notes, iconName, color, customFields)
                        }
                        onNavigateBack()
                    }
                }) {"""
btn_new = """                IconButton(onClick = {
                    if (!isSaving) {
                        isSaving = true
                        if (isTemplate) {
                            viewModel.addTemplate(title, username, password, url, notes, iconName, color, customFields)
                        } else if (isEdit) {
                            viewModel.updateEntry(title, username, password, url, notes, iconName, color, customFields)
                        } else {
                            viewModel.createEntry(title, username, password, url, notes, iconName, color, customFields)
                        }
                        onNavigateBack()
                    }
                }) {"""
content = content.replace(btn_old, btn_new)

title_old = """                title = { Text(if (isTemplate) "New Template" else "New Entry") },"""
title_new = """                title = { Text(if (isEdit) "Edit Entry" else if (isTemplate) "New Template" else "New Entry") },"""
content = content.replace(title_old, title_new)

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)
