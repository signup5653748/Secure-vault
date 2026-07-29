import re

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "r") as f:
    content = f.read()

# Make sure imports exist for shapes
if "import androidx.compose.foundation.shape.RoundedCornerShape" not in content:
    content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.foundation.shape.RoundedCornerShape\nimport androidx.compose.foundation.background\nimport androidx.compose.ui.graphics.Color")

# Replace bottomBar
new_bottom_bar = """        bottomBar = {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Left toolbar
                Surface(
                    shape = RoundedCornerShape(16.dp),
                    color = MaterialTheme.colorScheme.surfaceVariant,
                    modifier = Modifier.weight(1f).padding(end = 16.dp)
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp),
                        horizontalArrangement = Arrangement.SpaceEvenly,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        IconButton(onClick = { /* Lock */ }) {
                            Icon(Icons.Default.Lock, contentDescription = "Lock", tint = Color(0xFF0066FF))
                        }
                        IconButton(onClick = onNavigateBack) {
                            Icon(Icons.Default.Close, contentDescription = "Cancel")
                        }
                        IconButton(onClick = { showAttachmentsDialog = true }) {
                            Icon(Icons.Default.AttachFile, contentDescription = "Attachments")
                        }
                        IconButton(onClick = { showAddFieldDialog = true }) {
                            Icon(Icons.Default.Edit, contentDescription = "Add Field")
                        }
                        Box {
                            IconButton(onClick = { showMoreMenu = true }) {
                                Icon(Icons.Default.Menu, contentDescription = "More")
                            }
                            DropdownMenu(
                                expanded = showMoreMenu,
                                onDismissRequest = { showMoreMenu = false }
                            ) {
                                DropdownMenuItem(
                                    text = { Text("Generate Password") },
                                    onClick = { 
                                        showMoreMenu = false
                                        showPasswordGenerator = true 
                                    }
                                )
                                DropdownMenuItem(
                                    text = { Text("Set Icon & Color") },
                                    onClick = {
                                        showMoreMenu = false
                                        showIconColorDialog = true
                                    }
                                )
                            }
                        }
                    }
                }
                
                // Save Button
                FloatingActionButton(
                    onClick = {
                        viewModel.createEntry(
                            title = title,
                            username = username,
                            pass = password,
                            url = url,
                            notes = notes,
                            iconName = iconName,
                            color = color,
                            customFields = customFields
                        )
                        onNavigateBack()
                    },
                    containerColor = Color(0xFF0066FF),
                    contentColor = Color.White,
                    shape = RoundedCornerShape(16.dp),
                    modifier = Modifier.size(56.dp)
                ) {
                    Icon(Icons.Default.Check, contentDescription = "Save")
                }
            }
        }"""

content = re.sub(r'bottomBar = \{[\s\S]*?\}\n        \)', new_bottom_bar + "\n        )", content)

with open("app/src/main/java/com/example/ui/AddEntryScreen.kt", "w") as f:
    f.write(content)
