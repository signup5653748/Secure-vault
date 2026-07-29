import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

var_old = """    var showAttachmentsDialog by remember { mutableStateOf(false) }"""
var_new = """    var showAttachmentsDialog by remember { mutableStateOf(false) }
    var isSaving by remember { mutableStateOf(false) }"""
content = content.replace(var_old, var_new)

btn_old = """                IconButton(onClick = {
                    if (isTemplate) {
                        viewModel.addTemplate(title, username, password, url, notes, iconName, color, customFields)
                    } else {
                        viewModel.createEntry(title, username, password, url, notes, iconName, color, customFields)
                    }
                    onNavigateBack()
                }) {"""
btn_new = """                IconButton(onClick = {
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
content = content.replace(btn_old, btn_new)

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)
