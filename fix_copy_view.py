import re

with open('/app/applet/app/src/main/java/com/example/ui/ViewEntryScreen.kt', 'r') as f:
    content = f.read()

old_copy = """                                IconButton(onClick = { clipboardManager.setText(AnnotatedString(value.content)) }) {
                                    Icon(Icons.Default.ContentCopy, contentDescription = "Copy")
                                }"""

new_copy = """                                val showCopyButton = entry.customData["ShowCopyButton_${key}"]?.value?.toBooleanStrictOrNull() ?: true
                                if (showCopyButton) {
                                    IconButton(onClick = { clipboardManager.setText(AnnotatedString(value.content)) }) {
                                        Icon(Icons.Default.ContentCopy, contentDescription = "Copy")
                                    }
                                }"""

content = content.replace(old_copy, new_copy)

with open('/app/applet/app/src/main/java/com/example/ui/ViewEntryScreen.kt', 'w') as f:
    f.write(content)

