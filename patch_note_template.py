import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

# Replace the note template correctly
old_note = """                    customData = mapOf(
                        "ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Yellow"),
                        "Hide_UserName" to app.keemobile.kotpass.models.CustomDataValue("true"),
                        "Hide_Password" to app.keemobile.kotpass.models.CustomDataValue("true"),
                        "Hide_Url" to app.keemobile.kotpass.models.CustomDataValue("true")
                    ),
                    fields = EntryFields(mutableMapOf(
                        BasicField.Title() to EntryValue.Plain("Note"),
                        BasicField.UserName() to EntryValue.Plain(""),
                        BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString("")),
                        BasicField.Url() to EntryValue.Plain(""),
                        BasicField.Notes() to EntryValue.Plain(""),
                        "Note Content" to EntryValue.Plain("")
                    )),
                    customData = mapOf("TemplateType" to app.keemobile.kotpass.models.CustomDataValue("Note"), "ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Yellow"))"""

new_note = """                    fields = EntryFields(mutableMapOf(
                        BasicField.Title() to EntryValue.Plain("Note"),
                        BasicField.UserName() to EntryValue.Plain(""),
                        BasicField.Password() to EntryValue.Encrypted(EncryptedValue.fromString("")),
                        BasicField.Url() to EntryValue.Plain(""),
                        BasicField.Notes() to EntryValue.Plain(""),
                        "Note Content" to EntryValue.Plain("")
                    )),
                    customData = mapOf(
                        "TemplateType" to app.keemobile.kotpass.models.CustomDataValue("Note"), 
                        "ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Yellow"),
                        "Hide_UserName" to app.keemobile.kotpass.models.CustomDataValue("true"),
                        "Hide_Password" to app.keemobile.kotpass.models.CustomDataValue("true"),
                        "Hide_Url" to app.keemobile.kotpass.models.CustomDataValue("true")
                    )"""

content = content.replace(old_note, new_note)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
