import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

# Bank Account
bank_old = """                    icon = app.keemobile.kotpass.constants.PredefinedIcon.Money,
                    customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Green")),"""
bank_new = """                    icon = app.keemobile.kotpass.constants.PredefinedIcon.Money,
                    customData = mapOf(
                        "ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Green"),
                        "Hide_Url" to app.keemobile.kotpass.models.CustomDataValue("true")
                    ),"""
content = content.replace(bank_old, bank_new)

# Note
note_old = """                    icon = app.keemobile.kotpass.constants.PredefinedIcon.Note,
                    fields = EntryFields(mutableMapOf("""
note_new = """                    icon = app.keemobile.kotpass.constants.PredefinedIcon.Note,
                    customData = mapOf(
                        "ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Yellow"),
                        "Hide_UserName" to app.keemobile.kotpass.models.CustomDataValue("true"),
                        "Hide_Password" to app.keemobile.kotpass.models.CustomDataValue("true"),
                        "Hide_Url" to app.keemobile.kotpass.models.CustomDataValue("true")
                    ),
                    fields = EntryFields(mutableMapOf("""
content = content.replace(note_old, note_new)

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)
