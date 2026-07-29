import re

with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    text = f.read()

# Add ThemeColor to predefined templates
text = text.replace(
    'fields = EntryFields(mutableMapOf(\n                        BasicField.Title() to EntryValue.Plain("Gmail")',
    'customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Red")),\n                    fields = EntryFields(mutableMapOf(\n                        BasicField.Title() to EntryValue.Plain("Gmail")'
)

text = text.replace(
    'fields = EntryFields(mutableMapOf(\n                        BasicField.Title() to EntryValue.Plain("Facebook")',
    'customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Blue")),\n                    fields = EntryFields(mutableMapOf(\n                        BasicField.Title() to EntryValue.Plain("Facebook")'
)

text = text.replace(
    'fields = EntryFields(mutableMapOf(\n                        BasicField.Title() to EntryValue.Plain("Twitter")',
    'customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Cyan")),\n                    fields = EntryFields(mutableMapOf(\n                        BasicField.Title() to EntryValue.Plain("Twitter")'
)

text = text.replace(
    'fields = EntryFields(mutableMapOf(\n                        BasicField.Title() to EntryValue.Plain("Bank Account")',
    'customData = mapOf("ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Green")),\n                    fields = EntryFields(mutableMapOf(\n                        BasicField.Title() to EntryValue.Plain("Bank Account")'
)

text = text.replace(
    'customData = mapOf("TemplateType" to app.keemobile.kotpass.models.CustomDataValue("Note"))',
    'customData = mapOf("TemplateType" to app.keemobile.kotpass.models.CustomDataValue("Note"), "ThemeColor" to app.keemobile.kotpass.models.CustomDataValue("Yellow"))'
)

with open('app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(text)

