import re

with open('app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    text = f.read()

old_block = """                item {
                    var passVisible by remember { mutableStateOf(false) }
                    OutlinedTextField(
                        value = password,
                        onValueChange = { password = it },
                        label = { Text("Password") },
                        visualTransformation = if (passVisible) VisualTransformation.None else PasswordVisualTransformation(),
                        trailingIcon = {
                            Row {
                                IconButton(onClick = { passVisible = !passVisible }) {
                                    Icon(if (passVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, "Toggle Password")
                                }
                                IconButton(onClick = { clipboardManager.setText(AnnotatedString(password)) }) {
                                    Icon(Icons.Default.ContentCopy, "Copy Password")
                                }
                            }
                        },
                        modifier = Modifier.fillMaxWidth()
                    )
                }"""

new_block = """                item {
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
                        OutlinedTextField(
                            value = password,
                            onValueChange = { password = it },
                            label = { Text("Password") },
                            visualTransformation = if (passVisible) VisualTransformation.None else PasswordVisualTransformation(),
                            trailingIcon = {
                                Row {
                                    IconButton(onClick = { passVisible = !passVisible }) {
                                        Icon(if (passVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, "Toggle Password")
                                    }
                                    IconButton(onClick = { clipboardManager.setText(AnnotatedString(password)) }) {
                                        Icon(Icons.Default.ContentCopy, "Copy Password")
                                    }
                                }
                            },
                            modifier = Modifier.fillMaxWidth()
                        )
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
                }"""

text = text.replace(old_block, new_block)

with open('app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(text)

