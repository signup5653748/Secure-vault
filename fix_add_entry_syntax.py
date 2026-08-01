import re

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    content = f.read()

# Replace the broken section
target = """                newCustomFields.add(CustomFieldData(
                    name = fieldName,
                    value = fieldValue,
                    isHidden = isHidden,
                    showCopyButton = showCopy
    LaunchedEffect(selectedTemplate) {
        if (selectedTemplate != null && !isEdit) {
            val template = selectedTemplate!!
            title = template[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: ""
            username = template[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: ""
            password = template[app.keemobile.kotpass.constants.BasicField.Password]?.content ?: ""
            url = template[app.keemobile.kotpass.constants.BasicField.Url]?.content ?: ""
            notes = template[app.keemobile.kotpass.constants.BasicField.Notes]?.content ?: ""
            iconName = template.icon.name
            color = template.customData["ThemeColor"]?.value ?: "Blue"
            tagsString = template.tags.joinToString(", ")
            
            showUsername = template.customData["Hide_UserName"]?.value != "true"
            showPassword = template.customData["Hide_Password"]?.value != "true"
            showUrl = template.customData["Hide_Url"]?.value != "true"
            showNotes = template.customData["Hide_Notes"]?.value != "true"
            
            val newCustomFields = mutableListOf<CustomFieldData>()
            val basicFields = listOf(app.keemobile.kotpass.constants.BasicField.Title(), app.keemobile.kotpass.constants.BasicField.UserName(), app.keemobile.kotpass.constants.BasicField.Password(), app.keemobile.kotpass.constants.BasicField.Url(), app.keemobile.kotpass.constants.BasicField.Notes())
            
            for ((key, value) in template.fields) {
                if (key !in basicFields) {
                    val fieldName = key
                    val isHidden = value is app.keemobile.kotpass.models.EntryValue.Encrypted
                    val fieldValue = value.content
                    val showCopy = template.customData["ShowCopyButton_$fieldName"]?.value == "true"
                    newCustomFields.add(CustomFieldData(name = fieldName, value = fieldValue, isHidden = isHidden, showCopyButton = showCopy))
                }
            }
            customFields = newCustomFields
            viewModel.selectTemplateForNewEntry(null)
        }
    }
                ))
            }
        }
        newCustomFields
    } else {
        mutableListOf<CustomFieldData>()
    }
    }"""

replacement = """                newCustomFields.add(CustomFieldData(
                    name = fieldName,
                    value = fieldValue,
                    isHidden = isHidden,
                    showCopyButton = showCopy
                ))
            }
        }
        newCustomFields
    } else {
        mutableListOf<CustomFieldData>()
    }
    }

    LaunchedEffect(selectedTemplate) {
        if (selectedTemplate != null && !isEdit) {
            val template = selectedTemplate!!
            title = template[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: ""
            username = template[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: ""
            password = template[app.keemobile.kotpass.constants.BasicField.Password]?.content ?: ""
            url = template[app.keemobile.kotpass.constants.BasicField.Url]?.content ?: ""
            notes = template[app.keemobile.kotpass.constants.BasicField.Notes]?.content ?: ""
            iconName = template.icon.name
            color = template.customData["ThemeColor"]?.value ?: "Blue"
            tagsString = template.tags.joinToString(", ")
            
            showUsername = template.customData["Hide_UserName"]?.value != "true"
            showPassword = template.customData["Hide_Password"]?.value != "true"
            showUrl = template.customData["Hide_Url"]?.value != "true"
            showNotes = template.customData["Hide_Notes"]?.value != "true"
            
            val newCustomFields = mutableListOf<CustomFieldData>()
            val basicFields = listOf(app.keemobile.kotpass.constants.BasicField.Title(), app.keemobile.kotpass.constants.BasicField.UserName(), app.keemobile.kotpass.constants.BasicField.Password(), app.keemobile.kotpass.constants.BasicField.Url(), app.keemobile.kotpass.constants.BasicField.Notes())
            
            for ((key, value) in template.fields) {
                if (key !in basicFields) {
                    val fieldName = key
                    val isHidden = value is app.keemobile.kotpass.models.EntryValue.Encrypted
                    val fieldValue = value.content
                    val showCopy = template.customData["ShowCopyButton_$fieldName"]?.value == "true"
                    newCustomFields.add(CustomFieldData(name = fieldName, value = fieldValue, isHidden = isHidden, showCopyButton = showCopy))
                }
            }
            customFields = newCustomFields
            viewModel.selectTemplateForNewEntry(null)
        }
    }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(content)
print("fixed addentry syntax")
