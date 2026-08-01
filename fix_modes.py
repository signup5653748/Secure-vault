import re

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

# Add isReorderMode state
text = text.replace("var isDeleteMode by remember { mutableStateOf(false) }", 
                    "var isDeleteMode by remember { mutableStateOf(false) }\n    var isReorderMode by remember { mutableStateOf(false) }")

# Update Dropdown menu
menu_old = """                                DropdownMenuItem(
                                    text = { Text("Manage Fields") },
                                    onClick = {
                                        showMoreMenu = false
                                        isDeleteMode = true
                                        selectedFieldsToDelete = setOf()
                                    }
                                )"""

menu_new = """                                DropdownMenuItem(
                                    text = { Text("Delete Fields") },
                                    onClick = {
                                        showMoreMenu = false
                                        isDeleteMode = true
                                        isReorderMode = false
                                        selectedFieldsToDelete = setOf()
                                    }
                                )
                                DropdownMenuItem(
                                    text = { Text("Reorder Fields") },
                                    onClick = {
                                        showMoreMenu = false
                                        isReorderMode = true
                                        isDeleteMode = false
                                    }
                                )"""
text = text.replace(menu_old, menu_new)

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)

