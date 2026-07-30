import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

# Make Choose Template always visible
old_choose = """                actions = {
                    if (!isTemplate) {
                        TextButton(onClick = { showTemplateSheet = true }) {
                            Text("Choose Template")
                        }
                    }
                }"""

new_choose = """                actions = {
                    TextButton(onClick = { showTemplateSheet = true }) {
                        Text("Choose Template")
                    }
                }"""

content = content.replace(old_choose, new_choose)

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)
