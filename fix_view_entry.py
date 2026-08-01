with open("app/src/main/java/com/example/ui/ViewEntryScreen.kt", "r") as f:
    text = f.read()

text = text.replace('val basicKeys = setOf("Title", "UserName", "Password", "URL", "Notes")', 'val basicKeys = setOf(BasicField.Title(), BasicField.UserName(), BasicField.Password(), BasicField.Url(), BasicField.Notes())')

with open("app/src/main/java/com/example/ui/ViewEntryScreen.kt", "w") as f:
    f.write(text)
print("fixed view entry")
