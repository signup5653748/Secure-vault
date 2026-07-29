import re

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

# Replace the Scaffold floatingActionButton with the proper one without the Row
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
                },
                topBar = {"""

content = re.sub(r'Box\(modifier = Modifier\.fillMaxSize\(\)\) \{\s*Scaffold\(\s*floatingActionButton = \{[\s\S]*?\},?\s*topBar = \{', fab_code, content)

# Add Lock button to the Scaffold body
content = content.replace("LazyColumn(", """Box(modifier = Modifier.fillMaxSize()) {
                LazyColumn(""")

content = content.replace("""item { Spacer(modifier = Modifier.height(16.dp)) }
            }
        }""", """item { Spacer(modifier = Modifier.height(80.dp)) }
                }
                
                FloatingActionButton(
                    onClick = { viewModel.lockDatabase() },
                    containerColor = Color(0xFF0D47A1),
                    contentColor = Color.White,
                    shape = androidx.compose.foundation.shape.RoundedCornerShape(16.dp),
                    modifier = Modifier
                        .align(Alignment.BottomStart)
                        .padding(start = 16.dp, bottom = 16.dp)
                ) {
                    Icon(Icons.Default.Lock, contentDescription = "Lock")
                }
            }
        }""")

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
    f.write(content)
