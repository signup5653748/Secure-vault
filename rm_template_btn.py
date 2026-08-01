import re

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    content = f.read()

target = """                        TextButton(onClick = { showTemplateSheet = true }) {
                            Text("Choose Template")
                        }"""

content = content.replace(target, "")

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(content)
print("removed button")
