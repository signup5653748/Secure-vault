import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

# Modify CustomFieldData
content = content.replace(
    'data class CustomFieldData(val name: String, val value: String, val isHidden: Boolean, val showCopyButton: Boolean)',
    'data class CustomFieldData(val id: String = java.util.UUID.randomUUID().toString(), val name: String, val value: String, val isHidden: Boolean, val showCopyButton: Boolean)'
)

# Replace the items(customFields.size) block with items(customFields, key = { it.id })
old_items_block = r'            items\(customFields\.size\) \{ index ->\s+val field = customFields\[index\]\s+Card\(modifier = Modifier\.fillMaxWidth\(\)\) \{(.*?)\s+\}\s+\}'

# The regex captures everything inside the Card. We need to rebuild it carefully.
# Instead of regex, I can replace the specific strings.

content = content.replace(
    '            items(customFields.size) { index ->\n                val field = customFields[index]',
    '            items(customFields, key = { it.id }) { field ->'
)

content = content.replace(
    'customFields = customFields.filterIndexed { i, _ -> i != index }',
    'customFields = customFields.filter { it.id != field.id }'
)

# And in the creation:
content = content.replace(
    'customFields = customFields + CustomFieldData(fieldName, fieldValue, isHidden, showCopyButton)',
    'customFields = customFields + CustomFieldData(name = fieldName, value = fieldValue, isHidden = isHidden, showCopyButton = showCopyButton)'
)


with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)

