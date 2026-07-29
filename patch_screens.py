import re
import os

def patch_file(filepath, pattern, replacement):
    with open(filepath, 'r') as f:
        content = f.read()
    if pattern in content:
        content = content.replace(pattern, replacement)
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Patched {filepath}")
    else:
        print(f"Pattern not found in {filepath}")

# AddGroupScreen.kt
add_group_file = '/app/applet/app/src/main/java/com/example/ui/AddGroupScreen.kt'
add_group_var_old = """    var showIconDialog by remember { mutableStateOf(false) }"""
add_group_var_new = """    var showIconDialog by remember { mutableStateOf(false) }
    var isSaving by remember { mutableStateOf(false) }"""
patch_file(add_group_file, add_group_var_old, add_group_var_new)

add_group_btn_old = """                FloatingActionButton(
                    onClick = {
                        viewModel.createGroup(title, iconName, color)
                        onNavigateBack()
                    },
                    containerColor = Color(0xFF0066FF),"""
add_group_btn_new = """                FloatingActionButton(
                    onClick = {
                        if (!isSaving) {
                            isSaving = true
                            viewModel.createGroup(title, iconName, color)
                            onNavigateBack()
                        }
                    },
                    containerColor = Color(0xFF0066FF),"""
patch_file(add_group_file, add_group_btn_old, add_group_btn_new)

# AddNoteScreen.kt
add_note_file = '/app/applet/app/src/main/java/com/example/ui/AddNoteScreen.kt'
add_note_var_old = """    var color by remember { mutableStateOf("Blue") }"""
add_note_var_new = """    var color by remember { mutableStateOf("Blue") }
    var isSaving by remember { mutableStateOf(false) }"""
patch_file(add_note_file, add_note_var_old, add_note_var_new)

add_note_btn_old = """                FloatingActionButton(
                    onClick = {
                        viewModel.createEntry(
                            title = title,
                            username = "",
                            pass = "",
                            url = "",
                            notes = notes,
                            iconName = "Note",
                            color = color,
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
                                color = color,
                                customFields = emptyList()
                            )
                            onNavigateBack()
                        }
                    },"""
patch_file(add_note_file, add_note_btn_old, add_note_btn_new)
