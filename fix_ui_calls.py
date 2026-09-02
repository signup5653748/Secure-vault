import re

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

# Replace the save block
old_save = """                        if (isEdit && isTemplate) {
                                val hiddenFields = mutableListOf<String>()
                                if (!showUsername) hiddenFields.add("Hide_UserName")
                                if (!showPassword) hiddenFields.add("Hide_Password")
                                if (!showUrl) hiddenFields.add("Hide_Url")
                                if (!showNotes) hiddenFields.add("Hide_Notes")
                                
                                viewModel.updateEntry(title, username, password, url, notes, iconName, color, customFields, hiddenFields, tagsString.split(",").map { it.trim() }.filter { it.isNotEmpty() })
                            } else if (isEdit) {
                                val hiddenFields = mutableListOf<String>()
                                if (!showUsername) hiddenFields.add("Hide_UserName")
                                if (!showPassword) hiddenFields.add("Hide_Password")
                                if (!showUrl) hiddenFields.add("Hide_Url")
                                if (!showNotes) hiddenFields.add("Hide_Notes")
                                
                                viewModel.updateEntry(title, username, password, url, notes, iconName, color, customFields, hiddenFields, tagsString.split(",").map { it.trim() }.filter { it.isNotEmpty() })
                            } else if (isTemplate) {
                                val hiddenFields = mutableListOf<String>()
                                if (!showUsername) hiddenFields.add("Hide_UserName")
                                if (!showPassword) hiddenFields.add("Hide_Password")
                                if (!showUrl) hiddenFields.add("Hide_Url")
                                if (!showNotes) hiddenFields.add("Hide_Notes")
                                
                                viewModel.addTemplate(title, username, password, url, notes, iconName, color, customFields, hiddenFields, tagsString.split(",").map { it.trim() }.filter { it.isNotEmpty() })
                            } else {
                                val hiddenFields = mutableListOf<String>()
                                if (!showUsername) hiddenFields.add("Hide_UserName")
                                if (!showPassword) hiddenFields.add("Hide_Password")
                                if (!showUrl) hiddenFields.add("Hide_Url")
                                if (!showNotes) hiddenFields.add("Hide_Notes")
                                
                                viewModel.createEntry(title, username, password, url, notes, iconName, color, customFields, hiddenFields, tagsString.split(",").map { it.trim() }.filter { it.isNotEmpty() })
                            }"""

new_save = """                        val u = if (showUsername) username else null
                            val p = if (showPassword) password else null
                            val ur = if (showUrl) url else null
                            val n = if (showNotes) notes else null
                            val tagsList = tagsString.split(",").map { it.trim() }.filter { it.isNotEmpty() }
                            
                            if (isEdit && isTemplate) {
                                viewModel.updateEntry(title, u, p, ur, n, iconName, color, customFields, tagsList)
                            } else if (isEdit) {
                                viewModel.updateEntry(title, u, p, ur, n, iconName, color, customFields, tagsList)
                            } else if (isTemplate) {
                                viewModel.addTemplate(title, u, p, ur, n, iconName, color, customFields, tagsList)
                            } else {
                                viewModel.createEntry(title, u, p, ur, n, iconName, color, customFields, tagsList)
                            }"""

text = text.replace(old_save, new_save)

# Now for initial state, check if fields exist in entry.fields to determine showUsername etc.
# Old: var showUsername by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_UserName"]?.value != "true" else !isTemplate) }
old_show = """    var showUsername by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_UserName"]?.value != "true" else !isTemplate) }
    var showPassword by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_Password"]?.value != "true" else !isTemplate) }
    var showUrl by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_Url"]?.value != "true" else !isTemplate) }
    var showNotes by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_Notes"]?.value != "true" else !isTemplate) }"""

new_show = """    var showUsername by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.fields.containsKey(app.keemobile.kotpass.constants.BasicField.UserName()) && currentEntry!!.customData["Hide_UserName"]?.value != "true" else !isTemplate) }
    var showPassword by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.fields.containsKey(app.keemobile.kotpass.constants.BasicField.Password()) && currentEntry!!.customData["Hide_Password"]?.value != "true" else !isTemplate) }
    var showUrl by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.fields.containsKey(app.keemobile.kotpass.constants.BasicField.Url()) && currentEntry!!.customData["Hide_Url"]?.value != "true" else !isTemplate) }
    var showNotes by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.fields.containsKey(app.keemobile.kotpass.constants.BasicField.Notes()) && currentEntry!!.customData["Hide_Notes"]?.value != "true" else !isTemplate) }"""
text = text.replace(old_show, new_show)

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)

with open("app/src/main/java/com/example/ui/AddNoteScreen.kt", "r") as f:
    text2 = f.read()
old_add_note = """                            val hiddenFields = mutableListOf("Hide_UserName", "Hide_Password", "Hide_Url")
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
new_add_note = """                            viewModel.createEntry(
                                title = title,
                                username = null,
                                pass = null,
                                url = null,
                                notes = notes,
                                iconName = "Note",
                                color = "Blue",
                                customFields = emptyList()
                            )"""
text2 = text2.replace(old_add_note, new_add_note)
with open("app/src/main/java/com/example/ui/AddNoteScreen.kt", "w") as f:
    f.write(text2)

