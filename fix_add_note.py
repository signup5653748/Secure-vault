with open("app/src/main/java/com/example/ui/AddNoteScreen.kt", "r") as f:
    text = f.read()

import re

notes_old = """                            viewModel.createEntry(
                                title = title,
                                username = "",
                                pass = "",
                                url = "",
                                notes = notes,
                                iconName = "Note",
                                color = "Blue",
                                customFields = emptyList()
                            )"""

notes_new = """                            val hiddenFields = mutableListOf("Hide_UserName", "Hide_Password", "Hide_Url")
                            viewModel.createEntry(
                                title = title,
                                username = "",
                                pass = "",
                                url = "",
                                notes = notes,
                                iconName = "Note",
                                color = "Blue",
                                customFields = emptyList(),
                                hiddenFields = hiddenFields
                            )"""

text = text.replace(notes_old, notes_new)

with open("app/src/main/java/com/example/ui/AddNoteScreen.kt", "w") as f:
    f.write(text)

