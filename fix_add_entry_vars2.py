with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

vars_to_add = """    val predefinedIcons = listOf(
        "Key", "Lock", "Person", "CreditCard", 
        "Folder", "Mail", "Phone", "Build", 
        "Settings", "Favorite", "Star", "Home"
    )
"""

text = text.replace("    var isSaving by remember { mutableStateOf(false) }", vars_to_add + "    var isSaving by remember { mutableStateOf(false) }")

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)
print("icons added")
