import sys

with open('app/src/main/java/com/example/ui/VaultScreen.kt', 'r') as f:
    content = f.read()

target_vars = """    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)"""
replacement_vars = """    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
    var showUnsavedChangesDialog by remember { mutableStateOf(false) }
    var pendingAction by remember { mutableStateOf<(() -> Unit)?>(null) }
    
    if (showUnsavedChangesDialog) {
        AlertDialog(
            onDismissRequest = { showUnsavedChangesDialog = false },
            title = { Text("Unsaved Changes") },
            text = { Text("You have unsaved changes. Do you want to save them before proceeding?") },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.saveDatabase()
                    showUnsavedChangesDialog = false
                    pendingAction?.invoke()
                }) {
                    Text("Save Changes")
                }
            },
            dismissButton = {
                Row {
                    TextButton(onClick = { showUnsavedChangesDialog = false }) {
                        Text("Cancel")
                    }
                    TextButton(onClick = {
                        showUnsavedChangesDialog = false
                        pendingAction?.invoke()
                    }) {
                        Text("Discard")
                    }
                }
            }
        )
    }"""
content = content.replace(target_vars, replacement_vars)

target_close = """                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Lock, contentDescription = null) },
                    label = { Text("Close Vault") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        viewModel.lockDatabase()
                    }
                )"""
replacement_close = """                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Lock, contentDescription = null) },
                    label = { Text("Close Vault") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        if (hasUnsavedChanges) {
                            pendingAction = { viewModel.lockDatabase() }
                            showUnsavedChangesDialog = true
                        } else {
                            viewModel.lockDatabase()
                        }
                    }
                )"""
content = content.replace(target_close, replacement_close)

target_open = """                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.FolderOpen, contentDescription = null) },
                    label = { Text("Open Existing Vault") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        openFileLauncher.launch(arrayOf("application/octet-stream"))
                    }
                )"""
replacement_open = """                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.FolderOpen, contentDescription = null) },
                    label = { Text("Open Existing Vault") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        if (hasUnsavedChanges) {
                            pendingAction = { openFileLauncher.launch(arrayOf("application/octet-stream")) }
                            showUnsavedChangesDialog = true
                        } else {
                            openFileLauncher.launch(arrayOf("application/octet-stream"))
                        }
                    }
                )"""
content = content.replace(target_open, replacement_open)

with open('app/src/main/java/com/example/ui/VaultScreen.kt', 'w') as f:
    f.write(content)
print("Updated Vault UI with Unsaved Changes Dialog")
