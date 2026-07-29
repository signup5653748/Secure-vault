import re

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'r') as f:
    content = f.read()

# 1. Remove DropdownMenu from BottomAppBar
old_bottom_appbar = """                if (!isTemplate) {
                    Box {
                        IconButton(onClick = { showMoreMenu = true }) {
                            Icon(Icons.Default.MoreVert, contentDescription = "More")
                        }
                        DropdownMenu(
                            expanded = showMoreMenu,
                            onDismissRequest = { showMoreMenu = false }
                        ) {
                            DropdownMenuItem(
                                text = { Text("Generate Password") },
                                onClick = { 
                                    showPasswordGenerator = true
                                    showMoreMenu = false
                                },
                                leadingIcon = { Icon(Icons.Default.Build, contentDescription = null) }
                            )
                            // Add more items here if needed
                        }
                    }
                }"""

# Removing this block
content = content.replace(old_bottom_appbar, '')

# 2. Add generate password button inside the trailingIcon Row
old_trailing_icon = """                                Row {
                                    IconButton(onClick = { passVisible = !passVisible }) {
                                        Icon(if (passVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, "Toggle Password")
                                    }
                                    IconButton(onClick = { clipboardManager.setText(AnnotatedString(password)) }) {
                                        Icon(Icons.Default.ContentCopy, "Copy Password")
                                    }
                                }"""

new_trailing_icon = """                                Row {
                                    IconButton(onClick = { showPasswordGenerator = true }) {
                                        Icon(Icons.Default.Build, "Generate Password")
                                    }
                                    IconButton(onClick = { passVisible = !passVisible }) {
                                        Icon(if (passVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, "Toggle Password")
                                    }
                                    IconButton(onClick = { clipboardManager.setText(AnnotatedString(password)) }) {
                                        Icon(Icons.Default.ContentCopy, "Copy Password")
                                    }
                                }"""

content = content.replace(old_trailing_icon, new_trailing_icon)

with open('/app/applet/app/src/main/java/com/example/ui/AddEntryScreen.kt', 'w') as f:
    f.write(content)

