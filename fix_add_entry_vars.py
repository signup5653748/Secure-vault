with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

vars_to_add = """    var isDeleteMode by remember { mutableStateOf(false) }
    var selectedFieldsToDelete by remember { mutableStateOf(setOf<String>()) }
    var showPasswordGenerator by remember { mutableStateOf(false) }
    var showAddFieldDialog by remember { mutableStateOf(false) }
    var showIconDialog by remember { mutableStateOf(false) }
    var showColorDialog by remember { mutableStateOf(false) }
    var showAttachmentsDialog by remember { mutableStateOf(false) }
    var attachments by remember { mutableStateOf(listOf<String>()) }
    var showMoreMenu by remember { mutableStateOf(false) }
"""

text = text.replace("    var isSaving by remember { mutableStateOf(false) }", vars_to_add + "    var isSaving by remember { mutableStateOf(false) }")

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)
print("vars added")
