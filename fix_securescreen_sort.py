with open("app/src/main/java/com/example/ui/SecureScreen.kt", "r") as f:
    text = f.read()

import re

# We need to add sorting state and UI logic
imports = """import androidx.compose.ui.text.font.FontWeight
import androidx.compose.material.icons.filled.Sort"""

text = text.replace("import androidx.compose.ui.text.font.FontWeight", imports)

sort_state = """    var searchQuery by remember { mutableStateOf("") }
    var sortOrder by remember { mutableStateOf("Default") } // Default, A-Z, Z-A, Newest, Oldest
    var showSortMenu by remember { mutableStateOf(false) }"""

text = text.replace('    var searchQuery by remember { mutableStateOf("") }', sort_state)

top_bar_actions_old = """                            IconButton(onClick = { showSearch = true }) {
                                Icon(Icons.Default.Search, contentDescription = "Search")
                            }"""

top_bar_actions_new = """                            IconButton(onClick = { showSearch = true }) {
                                Icon(Icons.Default.Search, contentDescription = "Search")
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
                            }"""

text = text.replace(top_bar_actions_old, top_bar_actions_new)

sort_logic_old = """                        val entries = group.entries.filter {
                            it[app.keemobile.kotpass.constants.BasicField.Title]?.content?.contains(searchQuery, ignoreCase = true) == true
                        }
                        val groups = group.groups.filter {
                            it.name.contains(searchQuery, ignoreCase = true)
                        }"""

sort_logic_new = """                        val filteredEntries = group.entries.filter {
                            it[app.keemobile.kotpass.constants.BasicField.Title]?.content?.contains(searchQuery, ignoreCase = true) == true
                        }
                        val filteredGroups = group.groups.filter {
                            it.name.contains(searchQuery, ignoreCase = true)
                        }
                        
                        val groups = when (sortOrder) {
                            "A-Z" -> filteredGroups.sortedBy { it.name.lowercase() }
                            "Z-A" -> filteredGroups.sortedByDescending { it.name.lowercase() }
                            else -> filteredGroups
                        }
                        
                        val entries = when (sortOrder) {
                            "A-Z" -> filteredEntries.sortedBy { it[app.keemobile.kotpass.constants.BasicField.Title]?.content?.lowercase() ?: "" }
                            "Z-A" -> filteredEntries.sortedByDescending { it[app.keemobile.kotpass.constants.BasicField.Title]?.content?.lowercase() ?: "" }
                            else -> filteredEntries
                        }"""

text = text.replace(sort_logic_old, sort_logic_new)

with open("app/src/main/java/com/example/ui/SecureScreen.kt", "w") as f:
    f.write(text)

print("Added sorting")
