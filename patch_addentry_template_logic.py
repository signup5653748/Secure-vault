import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

template_load_old = """                                            notes = template[app.keemobile.kotpass.constants.BasicField.Notes]?.content ?: ""
                                            iconName = template.icon.name
                                            color = template.customData["ThemeColor"]?.value ?: "Blue"
                                            
                                            val newCustomFields = mutableListOf<CustomFieldData>()"""
template_load_new = """                                            notes = template[app.keemobile.kotpass.constants.BasicField.Notes]?.content ?: ""
                                            iconName = template.icon.name
                                            color = template.customData["ThemeColor"]?.value ?: "Blue"
                                            
                                            showUsername = template.customData["Hide_UserName"]?.value != "true"
                                            showPassword = template.customData["Hide_Password"]?.value != "true"
                                            showUrl = template.customData["Hide_Url"]?.value != "true"
                                            showNotes = template.customData["Hide_Notes"]?.value != "true"
                                            
                                            val newCustomFields = mutableListOf<CustomFieldData>()"""
content = content.replace(template_load_old, template_load_new)

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)
