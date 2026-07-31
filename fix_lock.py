import sys

with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

target = """    fun lockDatabase() {
        realSaveDatabase()

        if (settings.clipboardAutoClear.value) {"""
replacement = """    fun lockDatabase() {
        if (settings.clipboardAutoClear.value) {"""

content = content.replace(target, replacement)

with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
print("Updated lockDatabase")
