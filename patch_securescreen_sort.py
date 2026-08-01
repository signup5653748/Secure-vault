with open("app/src/main/java/com/example/ui/SecureScreen.kt", "r") as f:
    text = f.read()

import re

# Add state
state_old = """    val sheetState = rememberModalBottomSheetState()
    val scope = rememberCoroutineScope()"""
    
state_new = """    val sheetState = rememberModalBottomSheetState()
    val scope = rememberCoroutineScope()
    var sortOrder by remember { mutableStateOf("Default") }
    var showSortMenu by remember { mutableStateOf(false) }"""

text = text.replace(state_old, state_new)

# Add sort menu icon next to search
topbar_old = """                        IconButton(onClick = { viewModel.lockDatabase() }) {
                            Icon(Icons.Default.Lock, contentDescription = "Lock")
                        }"""
                        
topbar_new = """                        Box {
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
                        IconButton(onClick = { viewModel.lockDatabase() }) {
                            Icon(Icons.Default.Lock, contentDescription = "Lock")
                        }"""

text = text.replace(topbar_old, topbar_new)

# Apply sort logic
logic_old = """            val groups = currentGroup!!.groups
            val entries = currentGroup!!.entries"""
            
logic_new = """            val rawGroups = currentGroup!!.groups
            val rawEntries = currentGroup!!.entries
            
            val groups = when (sortOrder) {
                "A-Z" -> rawGroups.sortedBy { it.name.lowercase() }
                "Z-A" -> rawGroups.sortedByDescending { it.name.lowercase() }
                else -> rawGroups
            }
            
            val entries = when (sortOrder) {
                "A-Z" -> rawEntries.sortedBy { it[app.keemobile.kotpass.constants.BasicField.Title]?.content?.lowercase() ?: "" }
                "Z-A" -> rawEntries.sortedByDescending { it[app.keemobile.kotpass.constants.BasicField.Title]?.content?.lowercase() ?: "" }
                else -> rawEntries
            }"""

text = text.replace(logic_old, logic_new)

with open("app/src/main/java/com/example/ui/SecureScreen.kt", "w") as f:
    f.write(text)
    
