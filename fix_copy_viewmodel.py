import re

with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'customFields: List<Triple<String, String, Boolean>>',
    'customFields: List<com.example.ui.CustomFieldData>'
)

content = content.replace(
    'for (field in customFields) {\n            if (field.third) {\n                fieldsMap[field.first] = EntryValue.Encrypted(EncryptedValue.fromString(field.second))\n            } else {\n                fieldsMap[field.first] = EntryValue.Plain(field.second)\n            }\n        }',
    'for (field in customFields) {\n            if (field.isHidden) {\n                fieldsMap[field.name] = EntryValue.Encrypted(EncryptedValue.fromString(field.value))\n            } else {\n                fieldsMap[field.name] = EntryValue.Plain(field.value)\n            }\n        }'
)

old_custom_data = 'customData = mapOf("ThemeColor" to CustomDataValue(color))'
new_custom_data = 'customData = mapOf("ThemeColor" to CustomDataValue(color)) + customFields.associate { "ShowCopyButton_${it.name}" to CustomDataValue(it.showCopyButton.toString()) }'
content = content.replace(old_custom_data, new_custom_data)


with open('/app/applet/app/src/main/java/com/example/viewmodel/KeePassViewModel.kt', 'w') as f:
    f.write(content)

