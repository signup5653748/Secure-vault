with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

import re

save_logic_old = """                                                        if (isEdit) {
                                val hiddenFields = mutableListOf<String>()
                                if (!showUsername) hiddenFields.add("Hide_UserName")
                                if (!showPassword) hiddenFields.add("Hide_Password")
                                if (!showUrl) hiddenFields.add("Hide_Url")
                                if (!showNotes) hiddenFields.add("Hide_Notes")
                                
                                viewModel.updateEntry(title, username, password, url, notes, iconName, color, customFields, hiddenFields, tagsString.split(",").map { it.trim() }.filter { it.isNotEmpty() })
                            } else if (isTemplate) {"""

save_logic_new = """                                                        if (isEdit && isTemplate) {
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
                            } else if (isTemplate) {"""

text = text.replace(save_logic_old, save_logic_new)

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)

