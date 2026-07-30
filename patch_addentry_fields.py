import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

# Add state variables for visibility
state_vars_old = """    var customFields by remember { mutableStateOf("""
state_vars_new = """    var showUsername by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_UserName"]?.value != "true" else true) }
    var showPassword by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_Password"]?.value != "true" else true) }
    var showUrl by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_Url"]?.value != "true" else true) }
    var showNotes by remember { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["Hide_Notes"]?.value != "true" else true) }
    
    var customFields by remember { mutableStateOf("""
content = content.replace(state_vars_old, state_vars_new)

# Update the save button to pass hidden states (we will modify KeePassViewModel later)
save_old = """                            viewModel.addTemplate(title, username, password, url, notes, iconName, color, customFields)
                        } else if (isEdit) {
                            viewModel.updateEntry(title, username, password, url, notes, iconName, color, customFields)
                        } else {
                            viewModel.createEntry(title, username, password, url, notes, iconName, color, customFields)
                        }"""
save_new = """                            val hiddenFields = mutableListOf<String>()
                            if (!showUsername) hiddenFields.add("Hide_UserName")
                            if (!showPassword) hiddenFields.add("Hide_Password")
                            if (!showUrl) hiddenFields.add("Hide_Url")
                            if (!showNotes) hiddenFields.add("Hide_Notes")
                            
                            viewModel.addTemplate(title, username, password, url, notes, iconName, color, customFields, hiddenFields)
                        } else if (isEdit) {
                            val hiddenFields = mutableListOf<String>()
                            if (!showUsername) hiddenFields.add("Hide_UserName")
                            if (!showPassword) hiddenFields.add("Hide_Password")
                            if (!showUrl) hiddenFields.add("Hide_Url")
                            if (!showNotes) hiddenFields.add("Hide_Notes")
                            
                            viewModel.updateEntry(title, username, password, url, notes, iconName, color, customFields, hiddenFields)
                        } else {
                            val hiddenFields = mutableListOf<String>()
                            if (!showUsername) hiddenFields.add("Hide_UserName")
                            if (!showPassword) hiddenFields.add("Hide_Password")
                            if (!showUrl) hiddenFields.add("Hide_Url")
                            if (!showNotes) hiddenFields.add("Hide_Notes")
                            
                            viewModel.createEntry(title, username, password, url, notes, iconName, color, customFields, hiddenFields)
                        }"""
content = content.replace(save_old, save_new)

# Now, we need to wrap the UI for basic fields with an if condition and a delete button.
# Let's write a helper function or just use a custom row.
# We'll use a regex to replace each item block for basic fields.

# Username field
user_old = """            if (!isTemplate) {
                item {
                    OutlinedTextField(
                        value = username,
                        onValueChange = { username = it },
                        label = { Text("Username") },
                        modifier = Modifier.fillMaxWidth()
                    )
                }"""
user_new = """            if (showUsername) {
                item {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        OutlinedTextField(
                            value = username,
                            onValueChange = { username = it },
                            label = { Text("Username") },
                            modifier = Modifier.weight(1f)
                        )
                        if (isTemplate || isEdit || !isTemplate) {
                            IconButton(onClick = { showUsername = false; username = "" }) {
                                Icon(Icons.Default.Delete, contentDescription = "Remove Username", tint = Color.Red)
                            }
                        }
                    }
                }"""
content = content.replace(user_old, user_new)

# Password field
pass_old = """                item {
                    var passVisible by remember { mutableStateOf(false) }
                    OutlinedTextField(
                        value = password,
                        onValueChange = { password = it },
                        label = { Text("Password") },
                        visualTransformation = if (passVisible) androidx.compose.ui.text.input.VisualTransformation.None else androidx.compose.ui.text.input.PasswordVisualTransformation(),
                        modifier = Modifier.fillMaxWidth(),
                        trailingIcon = {
                            IconButton(onClick = { passVisible = !passVisible }) {
                                Icon(
                                    imageVector = if (passVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility,
                                    contentDescription = "Toggle password visibility"
                                )
                            }
                        }
                    )
                }"""
pass_new = """            if (showPassword) {
                item {
                    var passVisible by remember { mutableStateOf(false) }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        OutlinedTextField(
                            value = password,
                            onValueChange = { password = it },
                            label = { Text("Password") },
                            visualTransformation = if (passVisible) androidx.compose.ui.text.input.VisualTransformation.None else androidx.compose.ui.text.input.PasswordVisualTransformation(),
                            modifier = Modifier.weight(1f),
                            trailingIcon = {
                                IconButton(onClick = { passVisible = !passVisible }) {
                                    Icon(
                                        imageVector = if (passVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility,
                                        contentDescription = "Toggle password visibility"
                                    )
                                }
                            }
                        )
                        if (isTemplate || isEdit || !isTemplate) {
                            IconButton(onClick = { showPassword = false; password = "" }) {
                                Icon(Icons.Default.Delete, contentDescription = "Remove Password", tint = Color.Red)
                            }
                        }
                    }
                }
            }"""
content = content.replace(pass_old, pass_new)

# URL field
url_old = """            if (!isTemplate) {
                item {
                    OutlinedTextField(
                        value = url,
                        onValueChange = { url = it },
                        label = { Text("URL") },
                        modifier = Modifier.fillMaxWidth()
                    )
                }"""
url_new = """            if (showUrl) {
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
                }"""
content = content.replace(url_old, url_new)

# Notes field
notes_old = """            if (!isTemplate) {
                item {
                    OutlinedTextField(
                        value = notes,
                        onValueChange = { notes = it },
                        label = { Text("Notes") },
                        modifier = Modifier.fillMaxWidth(),
                        minLines = 3
                    )
                }
            }"""
notes_new = """            if (showNotes) {
                item {
                    Row(verticalAlignment = Alignment.Top) {
                        OutlinedTextField(
                            value = notes,
                            onValueChange = { notes = it },
                            label = { Text("Notes") },
                            modifier = Modifier.weight(1f),
                            minLines = 3
                        )
                        if (isTemplate || isEdit || !isTemplate) {
                            IconButton(onClick = { showNotes = false; notes = "" }) {
                                Icon(Icons.Default.Delete, contentDescription = "Remove Notes", tint = Color.Red)
                            }
                        }
                    }
                }
            }"""
content = content.replace(notes_old, notes_new)

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)
