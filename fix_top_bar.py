import re
with open("app/src/main/java/com/example/ui/ViewEntryScreen.kt", "r") as f:
    text = f.read()

old_topbar = """            TopAppBar(
                title = { Text((currentEntry?.get(BasicField.Title)?.content ?: "Entry")) },"""
new_topbar = """            TopAppBar(
                title = { Text("") },"""

text = text.replace(old_topbar, new_topbar)

with open("app/src/main/java/com/example/ui/ViewEntryScreen.kt", "w") as f:
    f.write(text)
