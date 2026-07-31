import sys

with open('app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

start_marker = "            if (showPassword) {"
end_marker = "            if (showNotes) {"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_block = """            if (showPassword) {
                item {
                    var passVisible by remember { mutableStateOf(false) }
                    val strength = when {
                        password.isEmpty() -> 0f
                        password.length < 8 -> 0.25f
                        password.length < 12 -> 0.5f
                        password.length < 16 -> 0.75f
                        else -> 1f
                    }
                    val strengthColor = when {
                        password.isEmpty() -> Color.Transparent
                        password.length < 8 -> Color.Red
                        password.length < 12 -> Color(0xFFFFA500)
                        password.length < 16 -> Color(0xFF9ACD32)
                        else -> Color.Green
                    }
                    Column(modifier = Modifier.fillMaxWidth()) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            OutlinedTextField(
                                value = password,
                                onValueChange = { password = it },
                                label = { Text("Password") },
                                visualTransformation = if (passVisible) VisualTransformation.None else PasswordVisualTransformation(),
                                trailingIcon = {
                                    Row {
                                        IconButton(onClick = { showPasswordGenerator = true }) {
                                            Icon(Icons.Default.Build, "Generate Password")
                                        }
                                        IconButton(onClick = { passVisible = !passVisible }) {
                                            Icon(if (passVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, "Toggle Password")
                                        }
                                        IconButton(onClick = { clipboardManager.setText(androidx.compose.ui.text.AnnotatedString(password)) }) {
                                            Icon(Icons.Default.ContentCopy, "Copy Password")
                                        }
                                    }
                                },
                                modifier = Modifier.weight(1f)
                            )
                            if (isTemplate || isEdit || !isTemplate) {
                                IconButton(onClick = { showPassword = false; password = "" }) {
                                    Icon(Icons.Default.Delete, contentDescription = "Remove Password", tint = Color.Red)
                                }
                            }
                        }
                        if (password.isNotEmpty()) {
                            LinearProgressIndicator(
                                progress = { strength },
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(horizontal = 8.dp, vertical = 4.dp)
                                    .height(4.dp)
                                    .clip(RoundedCornerShape(2.dp)),
                                color = strengthColor,
                                trackColor = MaterialTheme.colorScheme.surfaceVariant,
                            )
                        }
                    }
                }
            }
            if (showUrl) {
                item {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        OutlinedTextField(
                            value = url,
                            onValueChange = { url = it },
                            label = { Text("URL") },
                            modifier = Modifier.weight(1f)
                        )
                        if (isTemplate || isEdit || !isTemplate) {
                            IconButton(onClick = { showUrl = false; url = "" }) {
                                Icon(Icons.Default.Delete, contentDescription = "Remove URL", tint = Color.Red)
                            }
                        }
                    }
                }
            }
"""
    new_content = content[:start_idx] + new_block + content[end_idx:]
    with open('app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
        f.write(new_content)
    print("Fixed!")
else:
    print("Markers not found!")

