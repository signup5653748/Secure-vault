import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

# Fix addTemplate
add_old = "fun addTemplate(title: String, username: String, pass: String, url: String, notes: String, iconName: String, color: String, customFields: List<com.example.ui.CustomFieldData>)"
add_new = "fun addTemplate(title: String, username: String, pass: String, url: String, notes: String, iconName: String, color: String, customFields: List<com.example.ui.CustomFieldData>, hiddenFields: List<String> = emptyList())"
content = content.replace(add_old, add_new)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
