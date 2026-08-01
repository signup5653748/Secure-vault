import re

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    text = f.read()

# Add a state for order
order_state = """    var tagsString by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.tags.joinToString(", ") else "") }
    var fieldOrder by remember(currentEntry?.uuid) { mutableStateOf(listOf("Username", "Password", "URL", "Notes")) }"""

text = text.replace('    var tagsString by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.tags.joinToString(", ") else "") }', order_state)

# To properly sort, I have to refactor the hardcoded if statements to loop through fieldOrder
# I'll create a single `items(fieldOrder)` block instead of the 4 static blocks

static_blocks = """            if (showUsername) {
                item {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        if (isDeleteMode) {
                            Checkbox(checked = selectedFieldsToDelete.contains("Username"), onCheckedChange = { checked ->
                                if (checked) selectedFieldsToDelete = selectedFieldsToDelete + "Username" else selectedFieldsToDelete = selectedFieldsToDelete - "Username"
                            })
                        }
                        OutlinedTextField(
                            value = username,
                            onValueChange = { username = it },
                            label = { Text("Username") },
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
            }
            if (showPassword) {
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
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        if (isDeleteMode) {
                            Checkbox(checked = selectedFieldsToDelete.contains("Password"), onCheckedChange = { checked ->
                                if (checked) selectedFieldsToDelete = selectedFieldsToDelete + "Password" else selectedFieldsToDelete = selectedFieldsToDelete - "Password"
                            })
                        }
                        Column(modifier = Modifier.weight(1f)) {
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
            }
            if (showUrl) {
                item {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        if (isDeleteMode) {
                            Checkbox(checked = selectedFieldsToDelete.contains("URL"), onCheckedChange = { checked ->
                                if (checked) selectedFieldsToDelete = selectedFieldsToDelete + "URL" else selectedFieldsToDelete = selectedFieldsToDelete - "URL"
                            })
                        }
                        OutlinedTextField(
                            value = url,
                            onValueChange = { url = it },
                            label = { Text("URL") },
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
            }
            if (showNotes) {
                item {
                    Row(verticalAlignment = Alignment.Top) {
                        if (isDeleteMode) {
                            Checkbox(checked = selectedFieldsToDelete.contains("Notes"), onCheckedChange = { checked ->
                                if (checked) selectedFieldsToDelete = selectedFieldsToDelete + "Notes" else selectedFieldsToDelete = selectedFieldsToDelete - "Notes"
                            })
                        }
                        OutlinedTextField(
                            value = notes,
                            onValueChange = { notes = it },
                            label = { Text("Notes") },
                            modifier = Modifier.weight(1f),
                            minLines = 3
                        )
                    }
                }
            }"""

dynamic_blocks = """            items(fieldOrder.size) { index ->
                val field = fieldOrder[index]
                
                if (field == "Username" && showUsername) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        if (isDeleteMode) {
                            Column {
                                IconButton(onClick = { 
                                    if (index > 0) {
                                        val mutableOrder = fieldOrder.toMutableList()
                                        val temp = mutableOrder[index - 1]
                                        mutableOrder[index - 1] = mutableOrder[index]
                                        mutableOrder[index] = temp
                                        fieldOrder = mutableOrder
                                    }
                                }) {
                                    Icon(Icons.Default.KeyboardArrowUp, "Move Up")
                                }
                                IconButton(onClick = {
                                    if (index < fieldOrder.size - 1) {
                                        val mutableOrder = fieldOrder.toMutableList()
                                        val temp = mutableOrder[index + 1]
                                        mutableOrder[index + 1] = mutableOrder[index]
                                        mutableOrder[index] = temp
                                        fieldOrder = mutableOrder
                                    }
                                }) {
                                    Icon(Icons.Default.KeyboardArrowDown, "Move Down")
                                }
                            }
                            Checkbox(checked = selectedFieldsToDelete.contains("Username"), onCheckedChange = { checked ->
                                if (checked) selectedFieldsToDelete = selectedFieldsToDelete + "Username" else selectedFieldsToDelete = selectedFieldsToDelete - "Username"
                            })
                        }
                        OutlinedTextField(
                            value = username,
                            onValueChange = { username = it },
                            label = { Text("Username") },
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
                
                if (field == "Password" && showPassword) {
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
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        if (isDeleteMode) {
                            Column {
                                IconButton(onClick = { 
                                    if (index > 0) {
                                        val mutableOrder = fieldOrder.toMutableList()
                                        val temp = mutableOrder[index - 1]
                                        mutableOrder[index - 1] = mutableOrder[index]
                                        mutableOrder[index] = temp
                                        fieldOrder = mutableOrder
                                    }
                                }) {
                                    Icon(Icons.Default.KeyboardArrowUp, "Move Up")
                                }
                                IconButton(onClick = {
                                    if (index < fieldOrder.size - 1) {
                                        val mutableOrder = fieldOrder.toMutableList()
                                        val temp = mutableOrder[index + 1]
                                        mutableOrder[index + 1] = mutableOrder[index]
                                        mutableOrder[index] = temp
                                        fieldOrder = mutableOrder
                                    }
                                }) {
                                    Icon(Icons.Default.KeyboardArrowDown, "Move Down")
                                }
                            }
                            Checkbox(checked = selectedFieldsToDelete.contains("Password"), onCheckedChange = { checked ->
                                if (checked) selectedFieldsToDelete = selectedFieldsToDelete + "Password" else selectedFieldsToDelete = selectedFieldsToDelete - "Password"
                            })
                        }
                        Column(modifier = Modifier.weight(1f)) {
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
                
                if (field == "URL" && showUrl) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        if (isDeleteMode) {
                            Column {
                                IconButton(onClick = { 
                                    if (index > 0) {
                                        val mutableOrder = fieldOrder.toMutableList()
                                        val temp = mutableOrder[index - 1]
                                        mutableOrder[index - 1] = mutableOrder[index]
                                        mutableOrder[index] = temp
                                        fieldOrder = mutableOrder
                                    }
                                }) {
                                    Icon(Icons.Default.KeyboardArrowUp, "Move Up")
                                }
                                IconButton(onClick = {
                                    if (index < fieldOrder.size - 1) {
                                        val mutableOrder = fieldOrder.toMutableList()
                                        val temp = mutableOrder[index + 1]
                                        mutableOrder[index + 1] = mutableOrder[index]
                                        mutableOrder[index] = temp
                                        fieldOrder = mutableOrder
                                    }
                                }) {
                                    Icon(Icons.Default.KeyboardArrowDown, "Move Down")
                                }
                            }
                            Checkbox(checked = selectedFieldsToDelete.contains("URL"), onCheckedChange = { checked ->
                                if (checked) selectedFieldsToDelete = selectedFieldsToDelete + "URL" else selectedFieldsToDelete = selectedFieldsToDelete - "URL"
                            })
                        }
                        OutlinedTextField(
                            value = url,
                            onValueChange = { url = it },
                            label = { Text("URL") },
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
                
                if (field == "Notes" && showNotes) {
                    Row(verticalAlignment = Alignment.Top) {
                        if (isDeleteMode) {
                            Column {
                                IconButton(onClick = { 
                                    if (index > 0) {
                                        val mutableOrder = fieldOrder.toMutableList()
                                        val temp = mutableOrder[index - 1]
                                        mutableOrder[index - 1] = mutableOrder[index]
                                        mutableOrder[index] = temp
                                        fieldOrder = mutableOrder
                                    }
                                }) {
                                    Icon(Icons.Default.KeyboardArrowUp, "Move Up")
                                }
                                IconButton(onClick = {
                                    if (index < fieldOrder.size - 1) {
                                        val mutableOrder = fieldOrder.toMutableList()
                                        val temp = mutableOrder[index + 1]
                                        mutableOrder[index + 1] = mutableOrder[index]
                                        mutableOrder[index] = temp
                                        fieldOrder = mutableOrder
                                    }
                                }) {
                                    Icon(Icons.Default.KeyboardArrowDown, "Move Down")
                                }
                            }
                            Checkbox(checked = selectedFieldsToDelete.contains("Notes"), onCheckedChange = { checked ->
                                if (checked) selectedFieldsToDelete = selectedFieldsToDelete + "Notes" else selectedFieldsToDelete = selectedFieldsToDelete - "Notes"
                            })
                        }
                        OutlinedTextField(
                            value = notes,
                            onValueChange = { notes = it },
                            label = { Text("Notes") },
                            modifier = Modifier.weight(1f),
                            minLines = 3
                        )
                    }
                }
            }"""

text = text.replace(static_blocks, dynamic_blocks)

# Also import missing icons
if "import androidx.compose.material.icons.filled.KeyboardArrowUp" not in text:
    text = text.replace("import androidx.compose.material.icons.filled.Delete", "import androidx.compose.material.icons.filled.Delete\nimport androidx.compose.material.icons.filled.KeyboardArrowUp\nimport androidx.compose.material.icons.filled.KeyboardArrowDown")

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(text)

