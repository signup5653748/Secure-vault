import re

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

# Add showPasswordGenerator state
target_state = "var showChangePasswordDialog by remember { mutableStateOf(false) }"
replacement_state = target_state + "\n    var showPasswordGenerator by remember { mutableStateOf(false) }"
content = content.replace(target_state, replacement_state)

# Replace the newPass textfield
target_textfield = """                                OutlinedTextField(
                                    value = newPass,
                                    onValueChange = { newPass = it },
                                    label = { Text("New Password") },
                                    visualTransformation = if (newPassVisible) androidx.compose.ui.text.input.VisualTransformation.None else androidx.compose.ui.text.input.PasswordVisualTransformation(),
                                    trailingIcon = {
                                        IconButton(onClick = { newPassVisible = !newPassVisible }) {
                                            Icon(if (newPassVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, "Toggle Password")
                                        }
                                    }
                                )"""

replacement_textfield = """                                Column(modifier = Modifier.fillMaxWidth()) {
                                    OutlinedTextField(
                                        value = newPass,
                                        onValueChange = { newPass = it },
                                        label = { Text("New Password") },
                                        visualTransformation = if (newPassVisible) androidx.compose.ui.text.input.VisualTransformation.None else androidx.compose.ui.text.input.PasswordVisualTransformation(),
                                        trailingIcon = {
                                            Row {
                                                IconButton(onClick = { showPasswordGenerator = true }) {
                                                    Icon(Icons.Default.Build, "Generate Password")
                                                }
                                                IconButton(onClick = { newPassVisible = !newPassVisible }) {
                                                    Icon(if (newPassVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, "Toggle Password")
                                                }
                                            }
                                        },
                                        modifier = Modifier.fillMaxWidth()
                                    )
                                    val strength = when {
                                        newPass.isEmpty() -> 0f
                                        newPass.length < 8 -> 0.25f
                                        newPass.length < 12 -> 0.5f
                                        newPass.length < 16 -> 0.75f
                                        else -> 1f
                                    }
                                    val strengthColor = when {
                                        newPass.isEmpty() -> Color.Transparent
                                        newPass.length < 8 -> Color.Red
                                        newPass.length < 12 -> Color(0xFFFFA500)
                                        newPass.length < 16 -> Color(0xFF9ACD32)
                                        else -> Color.Green
                                    }
                                    if (newPass.isNotEmpty()) {
                                        LinearProgressIndicator(
                                            progress = { strength },
                                            color = strengthColor,
                                            modifier = Modifier.fillMaxWidth().height(4.dp).padding(top = 4.dp)
                                        )
                                    }
                                }"""

content = content.replace(target_textfield, replacement_textfield)


generator_dialog = """                if (showPasswordGenerator) {
                    var passLength by remember { mutableStateOf(16f) }
                    var useUpper by remember { mutableStateOf(true) }
                    var useLower by remember { mutableStateOf(true) }
                    var useNumbers by remember { mutableStateOf(true) }
                    var useSymbols by remember { mutableStateOf(true) }
                    var excludeSimilar by remember { mutableStateOf(false) }
                    
                    var generatedPassword by remember { mutableStateOf("") }
                    
                    val strength = when {
                        passLength < 8 -> "Weak"
                        passLength < 12 -> "Medium"
                        passLength < 16 -> "Strong"
                        else -> "Excellent"
                    }
                    
                    val strengthColor = when(strength) {
                        "Weak" -> Color.Red
                        "Medium" -> Color(0xFFFFA500) // Orange
                        "Strong" -> Color(0xFF9ACD32) // YellowGreen
                        else -> Color.Green
                    }

                    fun generateNewPass() {
                        var upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                        var lower = "abcdefghijklmnopqrstuvwxyz"
                        var numbers = "0123456789"
                        var symbols = "!@#$%^&*()-_+="
                        if (excludeSimilar) {
                            upper = upper.filter { it !in "IO" }
                            lower = lower.filter { it !in "l1o0" }
                            numbers = numbers.filter { it !in "10" }
                            symbols = symbols.filter { it !in "|I" }
                        }
                        var chars = ""
                        if (useUpper) chars += upper
                        if (useLower) chars += lower
                        if (useNumbers) chars += numbers
                        if (useSymbols) chars += symbols
                        if (chars.isEmpty()) chars = lower
                        
                        var genPass = ""
                        for (i in 0 until passLength.toInt()) {
                            genPass += chars.random()
                        }
                        generatedPassword = genPass
                    }
                    
                    LaunchedEffect(passLength, useUpper, useLower, useNumbers, useSymbols, excludeSimilar) {
                        generateNewPass()
                    }

                    AlertDialog(
                        onDismissRequest = { showPasswordGenerator = false },
                        title = { Text("Password Generator") },
                        text = {
                            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                Text(generatedPassword, fontSize = 18.sp, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold, modifier = Modifier.align(Alignment.CenterHorizontally))
                                Text("Length: ${passLength.toInt()}")
                                Slider(
                                    value = passLength,
                                    onValueChange = { passLength = it },
                                    valueRange = 4f..64f
                                )
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Checkbox(checked = useUpper, onCheckedChange = { useUpper = it })
                                    Text("Uppercase")
                                }
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Checkbox(checked = useLower, onCheckedChange = { useLower = it })
                                    Text("Lowercase")
                                }
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Checkbox(checked = useNumbers, onCheckedChange = { useNumbers = it })
                                    Text("Numbers")
                                }
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Checkbox(checked = useSymbols, onCheckedChange = { useSymbols = it })
                                    Text("Symbols")
                                }
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Checkbox(checked = excludeSimilar, onCheckedChange = { excludeSimilar = it })
                                    Text("Exclude similar characters")
                                }
                                Text("Strength: $strength", color = strengthColor, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                            }
                        },
                        confirmButton = {
                            Row {
                                TextButton(onClick = {
                                    androidx.compose.ui.platform.LocalClipboardManager.current.setText(androidx.compose.ui.text.AnnotatedString(generatedPassword))
                                }) { Text("Copy") }
                                TextButton(onClick = {
                                    newPass = generatedPassword
                                    showPasswordGenerator = false
                                }) { Text("Use Password") }
                            }
                        },
                        dismissButton = {
                            TextButton(onClick = { showPasswordGenerator = false }) { Text("Cancel") }
                        }
                    )
                }"""

# Insert generator_dialog below the AlertDialog
target_insert = "showChangePasswordDialog = false\n                            }\n                        }\n                    )\n                }"
replacement_insert = target_insert + "\n" + generator_dialog

content = content.replace(target_insert, replacement_insert)

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
    f.write(content)
print("patched vault password generator")
