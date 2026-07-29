import re

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

# Add remember for FAB menu
content = content.replace("var showNewGroupDialog by remember { mutableStateOf(false) }", """var showNewGroupDialog by remember { mutableStateOf(false) }
    var showFabMenu by remember { mutableStateOf(false) }""")

# Remove the lock button from top bar
content = content.replace("""                        IconButton(onClick = { viewModel.lockDatabase() }) {
                            Icon(Icons.Default.Lock, contentDescription = "Lock")
                        }""", "")

# Add Box for scrim and update FAB
fab_code = """
        Box(modifier = Modifier.fillMaxSize()) {
            Scaffold(
                floatingActionButton = {
                    Column(horizontalAlignment = Alignment.End) {
                        if (showFabMenu) {
                            ExtendedFloatingActionButton(
                                text = { Text("Add entry") },
                                icon = { Icon(Icons.Default.VpnKey, "Add entry") },
                                onClick = { 
                                    showFabMenu = false
                                    onNavigateToAddEntry()
                                },
                                containerColor = Color(0xFF0066FF),
                                contentColor = Color.White,
                                modifier = Modifier.padding(bottom = 16.dp)
                            )
                            ExtendedFloatingActionButton(
                                text = { Text("Add group") },
                                icon = { Icon(Icons.Default.Folder, "Add group") },
                                onClick = {
                                    showFabMenu = false
                                    showNewGroupDialog = true
                                },
                                containerColor = Color(0xFF0066FF),
                                contentColor = Color.White,
                                modifier = Modifier.padding(bottom = 16.dp)
                            )
                        }
                        
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            FloatingActionButton(
                                onClick = { viewModel.lockDatabase() },
                                containerColor = Color(0xFF0D47A1),
                                contentColor = Color.White,
                                shape = androidx.compose.foundation.shape.RoundedCornerShape(16.dp),
                                modifier = Modifier.padding(start = 32.dp)
                            ) {
                                Icon(Icons.Default.Lock, contentDescription = "Lock")
                            }
                            FloatingActionButton(
                                onClick = { showFabMenu = !showFabMenu },
                                containerColor = if (showFabMenu) Color(0xFF0066FF) else Color(0xFF0D47A1),
                                contentColor = Color.White,
                                shape = CircleShape
                            ) {
                                Icon(
                                    if (showFabMenu) Icons.Default.Close else Icons.Default.Add, 
                                    contentDescription = if (showFabMenu) "Close" else "Add"
                                )
                            }
                        }
                    }
                },
                topBar = {"""

content = re.sub(r'Scaffold\(\s*floatingActionButton = \{[\s\S]*?\},?\s*topBar = \{', fab_code, content)

# Scrim over the list
scrim_code = """            if (showFabMenu) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.Black.copy(alpha = 0.5f))
                        .clickable(
                            interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                            indication = null
                        ) { showFabMenu = false }
                )
            }
        }
    }
}

@Composable
"""

content = content.replace("""            }
        }
    }
}

@Composable
""", scrim_code)

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
    f.write(content)
