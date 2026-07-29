import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

# Add CustomFieldData data class
content = content.replace('import com.example.viewmodel.KeePassViewModel\n', 'import com.example.viewmodel.KeePassViewModel\n\ndata class CustomFieldData(val name: String, val value: String, val isHidden: Boolean, val showCopyButton: Boolean)\n')

# Change state variable
content = content.replace('var customFields by remember { mutableStateOf(listOf<Triple<String, String, Boolean>>()) }', 'var customFields by remember { mutableStateOf(listOf<CustomFieldData>()) }')

# Fix items(customFields)
old_items = """            items(customFields) { field ->
                Card(modifier = Modifier.fillMaxWidth()) {
                    var isVisible by remember { mutableStateOf(false) }
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(field.first, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                if (field.third && !isVisible) "••••••••" else field.second, 
                                modifier = Modifier.weight(1f),
                                fontSize = 16.sp
                            )
                            if (field.third) {
                                IconButton(onClick = { isVisible = !isVisible }) {
                                    Icon(if (isVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, "Toggle Visibility")
                                }
                            }
                            IconButton(onClick = { clipboardManager.setText(AnnotatedString(field.second)) }) {
                                Icon(Icons.Default.ContentCopy, "Copy")
                            }
                            IconButton(onClick = {
                                customFields = customFields.filter { it != field }
                            }) {
                                Icon(Icons.Default.Delete, "Delete")
                            }
                        }
                    }
                }
            }"""

new_items = """            items(customFields.size) { index ->
                val field = customFields[index]
                Card(modifier = Modifier.fillMaxWidth()) {
                    var isVisible by remember { mutableStateOf(false) }
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(field.name, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text(
                                if (field.isHidden && !isVisible) "••••••••" else field.value, 
                                modifier = Modifier.weight(1f),
                                fontSize = 16.sp
                            )
                            if (field.isHidden) {
                                IconButton(onClick = { isVisible = !isVisible }) {
                                    Icon(if (isVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, "Toggle Visibility")
                                }
                            }
                            if (field.showCopyButton) {
                                IconButton(onClick = { clipboardManager.setText(AnnotatedString(field.value)) }) {
                                    Icon(Icons.Default.ContentCopy, "Copy")
                                }
                            }
                            IconButton(onClick = {
                                customFields = customFields.filterIndexed { i, _ -> i != index }
                            }) {
                                Icon(Icons.Default.Delete, "Delete")
                            }
                        }
                    }
                }
            }"""

content = content.replace(old_items, new_items)

# Fix adding field
content = content.replace('customFields = customFields + Triple(fieldName, fieldValue, isHidden)', 'customFields = customFields + CustomFieldData(fieldName, fieldValue, isHidden, showCopyButton)')

# Fix saving
old_save = """                    if (isTemplate) {
                        viewModel.addTemplate(title, username, password, url, notes, iconName, color, customFields)
                    } else {
                        viewModel.createEntry(title, username, password, url, notes, iconName, color, customFields)
                    }"""

new_save = """                    val mappedFields = customFields.map { Triple(it.name, it.value, it.isHidden) }
                    if (isTemplate) {
                        viewModel.addTemplate(title, username, password, url, notes, iconName, color, mappedFields)
                    } else {
                        viewModel.createEntry(title, username, password, url, notes, iconName, color, mappedFields)
                    }"""

content = content.replace(old_save, new_save)

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)

