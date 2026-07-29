#!/bin/bash
sed -i 's/TemplateType" to app.keemobile.kotpass.models.CustomDataValue("Note"))/TemplateType" to app.keemobile.kotpass.models.CustomDataValue("Note"), "ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Yellow"))/' app/src/main/java/com/example/viewmodel/KeePassViewModel.kt

sed -i 's/BasicField.Title() to EntryValue.Plain("Gmail"),/BasicField.Title() to EntryValue.Plain("Gmail"),\n                        "ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Red"),/g' app/src/main/java/com/example/viewmodel/KeePassViewModel.kt
# Actually, it's easier to use sed to add ThemeColor to the customData map for the other predefined templates.
