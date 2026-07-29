import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

old_clickable = """                                    .clickable {
                                        title = template[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: ""
                                        username = template[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: ""
                                        url = template[app.keemobile.kotpass.constants.BasicField.Url]?.content ?: ""
                                        notes = template[app.keemobile.kotpass.constants.BasicField.Notes]?.content ?: ""
                                        iconName = template.icon.name
                                        color = template.customData["ThemeColor"]?.value ?: "Blue"
                                        
                                        val newCustomFields = mutableListOf<CustomFieldData>()
                                        val basicFields = listOf(app.keemobile.kotpass.constants.BasicField.Title(), app.keemobile.kotpass.constants.BasicField.UserName(), app.keemobile.kotpass.constants.BasicField.Password(), app.keemobile.kotpass.constants.BasicField.Url(), app.keemobile.kotpass.constants.BasicField.Notes())
                                        template.fields.entries.forEach { (key, value) ->
                                            if (key !in basicFields) {
                                                val fieldName = key
                                                val isHidden = value is app.keemobile.kotpass.models.EntryValue.Encrypted
                                                val fieldValue = value.content
                                                val showCopy = template.customData["ShowCopyButton_$fieldName"]?.value == "true"
                                                newCustomFields.add(CustomFieldData(name = fieldName, value = fieldValue, isHidden = isHidden, showCopyButton = showCopy))
                                            }
                                        }
                                        customFields = newCustomFields
                                        
                                        scope.launch { templateSheetState.hide() }.invokeOnCompletion {
                                            if (!templateSheetState.isVisible) {
                                                showTemplateSheet = false
                                            }
                                        }
                                    },"""

new_clickable = """                                    .clickable {
                                        try {
                                            title = template[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: ""
                                            username = template[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: ""
                                            password = template[app.keemobile.kotpass.constants.BasicField.Password]?.content ?: ""
                                            url = template[app.keemobile.kotpass.constants.BasicField.Url]?.content ?: ""
                                            notes = template[app.keemobile.kotpass.constants.BasicField.Notes]?.content ?: ""
                                            iconName = template.icon.name
                                            color = template.customData["ThemeColor"]?.value ?: "Blue"
                                            
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
                                            
                                            scope.launch { templateSheetState.hide() }.invokeOnCompletion {
                                                if (!templateSheetState.isVisible) {
                                                    showTemplateSheet = false
                                                }
                                            }
                                        } catch (e: Exception) {
                                            android.util.Log.e("AddEntryScreen", "Error loading template", e)
                                        }
                                    },"""

content = content.replace(old_clickable, new_clickable)

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)
