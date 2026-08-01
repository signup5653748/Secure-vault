with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

old_save_logic = """                            if (isTemplate) {
                                val hiddenFields = mutableListOf<String>()
                                if (!showUsername) hiddenFields.add("Hide_UserName")
                                if (!showPassword) hiddenFields.add("Hide_Password")
                                if (!showUrl) hiddenFields.add("Hide_Url")
                                if (!showNotes) hiddenFields.add("Hide_Notes")
                                
                                viewModel.addTemplate(title, username, password, url, notes, iconName, color, customFields, hiddenFields, tagsString.split(",").map { it.trim() }.filter { it.isNotEmpty() })
                            } else if (isEdit) {"""

new_save_logic = """                            if (isEdit) {
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
                            } else {"""

text = text.replace(old_save_logic, new_save_logic)

# Replace the generic `else` block we broke
old_else = """                                viewModel.updateEntry(title, username, password, url, notes, iconName, color, customFields, hiddenFields, tagsString.split(",").map { it.trim() }.filter { it.isNotEmpty() })
                            } else {
                                val hiddenFields = mutableListOf<String>()"""

new_else = """                                val hiddenFields = mutableListOf<String>()"""

text = text.replace(old_else, new_else)

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)

