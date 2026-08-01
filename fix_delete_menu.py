with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

text = text.replace('text = { Text("Delete Fields") }', 'text = { Text("Manage Fields") }')
text = text.replace('Text("Delete Selected Fields")', 'Text("Delete / Done")')

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)
