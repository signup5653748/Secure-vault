import re

with open('/app/applet/app/src/main/java/com/example/ui/AddNoteScreen.kt', 'r') as f:
    content = f.read()

add_note_var_old = """    var notes by remember { mutableStateOf("") }"""
add_note_var_new = """    var notes by remember { mutableStateOf("") }
    var isSaving by remember { mutableStateOf(false) }"""
content = content.replace(add_note_var_old, add_note_var_new)

add_note_btn_old = """                FloatingActionButton(
                    onClick = {
                        viewModel.createEntry(
                            title = title,
                            username = "",
                            pass = "",
                            url = "",
                            notes = notes,
                            iconName = "Note",
                            color = "Blue",
                            customFields = emptyList()
                        )
                        onNavigateBack()
                    },"""
add_note_btn_new = """                FloatingActionButton(
                    onClick = {
                        if (!isSaving) {
                            isSaving = true
                            viewModel.createEntry(
                                title = title,
                                username = "",
                                pass = "",
                                url = "",
                                notes = notes,
                                iconName = "Note",
                                color = "Blue",
                                customFields = emptyList()
                            )
                            onNavigateBack()
                        }
                    },"""
content = content.replace(add_note_btn_old, add_note_btn_new)

with open('/app/applet/app/src/main/java/com/example/ui/AddNoteScreen.kt', 'w') as f:
    f.write(content)
