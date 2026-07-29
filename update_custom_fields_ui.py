import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

old_custom_fields = """            items(customFields, key = { it.id }) { field ->
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
                                customFields = customFields.filter { it.id != field.id }
                            }) {
                                Icon(Icons.Default.Delete, "Delete")
                            }
                        }
                    }
                }
            }"""

new_custom_fields = """            items(customFields, key = { it.id }) { field ->
                var isVisible by remember { mutableStateOf(!field.isHidden) }
                OutlinedTextField(
                    value = field.value,
                    onValueChange = { newValue -> 
                        customFields = customFields.map { 
                            if (it.id == field.id) it.copy(value = newValue) else it 
                        }
                    },
                    label = { Text(field.name) },
                    visualTransformation = if (!isVisible && field.isHidden) PasswordVisualTransformation() else VisualTransformation.None,
                    trailingIcon = {
                        Row {
                            if (field.isHidden) {
                                IconButton(onClick = { isVisible = !isVisible }) {
                                    Icon(if (isVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, contentDescription = "Toggle Visibility")
                                }
                            }
                            IconButton(onClick = {
                                customFields = customFields.filter { it.id != field.id }
                            }) {
                                Icon(Icons.Default.Delete, "Delete")
                            }
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    shape = RoundedCornerShape(12.dp)
                )
            }"""

content = content.replace(old_custom_fields, new_custom_fields)

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)
