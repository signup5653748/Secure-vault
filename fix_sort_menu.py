with open("app/src/main/java/com/example/ui/SecureScreen.kt", "r") as f:
    text = f.read()

# Add sort menu icon
import_to_add = "import androidx.compose.material.icons.filled.Sort"
if import_to_add not in text:
    text = text.replace("import androidx.compose.material.icons.filled.Lock", "import androidx.compose.material.icons.filled.Lock\n" + import_to_add)
    
menu_old = """                        IconButton(onClick = { viewModel.saveDatabase() }) {
                            if (hasUnsavedChanges) {
                                BadgedBox(badge = { Badge { Text("!") } }) {
                                    Icon(Icons.Default.Save, contentDescription = "Save", tint = MaterialTheme.colorScheme.primary)
                                }
                            } else {
                                Icon(Icons.Default.Save, contentDescription = "Save")
                            }
                        }
                        IconButton(onClick = onNavigateToSettings) {
                            Icon(Icons.Default.Settings, contentDescription = "Settings")
                        }"""

menu_new = """                        IconButton(onClick = { viewModel.saveDatabase() }) {
                            if (hasUnsavedChanges) {
                                BadgedBox(badge = { Badge { Text("!") } }) {
                                    Icon(Icons.Default.Save, contentDescription = "Save", tint = MaterialTheme.colorScheme.primary)
                                }
                            } else {
                                Icon(Icons.Default.Save, contentDescription = "Save")
                            }
                        }
                        Box {
                            IconButton(onClick = { showSortMenu = true }) {
                                Icon(Icons.Default.Sort, contentDescription = "Sort")
                            }
                            DropdownMenu(
                                expanded = showSortMenu,
                                onDismissRequest = { showSortMenu = false }
                            ) {
                                DropdownMenuItem(
                                    text = { Text("Default") },
                                    onClick = { sortOrder = "Default"; showSortMenu = false }
                                )
                                DropdownMenuItem(
                                    text = { Text("A-Z") },
                                    onClick = { sortOrder = "A-Z"; showSortMenu = false }
                                )
                                DropdownMenuItem(
                                    text = { Text("Z-A") },
                                    onClick = { sortOrder = "Z-A"; showSortMenu = false }
                                )
                            }
                        }
                        IconButton(onClick = onNavigateToSettings) {
                            Icon(Icons.Default.Settings, contentDescription = "Settings")
                        }"""

text = text.replace(menu_old, menu_new)

with open("app/src/main/java/com/example/ui/SecureScreen.kt", "w") as f:
    f.write(text)

print("Fixed sort menu")
