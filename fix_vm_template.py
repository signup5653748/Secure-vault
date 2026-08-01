import re

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "r") as f:
    content = f.read()

target = "fun selectEntry(entry: Entry) {"
replacement = """    private val _selectedTemplate = MutableStateFlow<Entry?>(null)
    val selectedTemplate = _selectedTemplate.asStateFlow()

    fun selectTemplateForNewEntry(template: Entry?) {
        _selectedTemplate.value = template
    }

    fun selectEntry(entry: Entry) {"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/viewmodel/KeePassViewModel.kt", "w") as f:
    f.write(content)
print("fixed vm template")
