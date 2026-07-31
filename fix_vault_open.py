import sys

with open('app/src/main/java/com/example/ui/VaultScreen.kt', 'r') as f:
    content = f.read()

target_open = """                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.FolderOpen, contentDescription = null) },
                    label = { Text("Open Existing Vault") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        filePickerLauncher.launch(arrayOf("*/*"))
                    }
                )"""
replacement_open = """                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.FolderOpen, contentDescription = null) },
                    label = { Text("Open Existing Vault") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        if (hasUnsavedChanges) {
                            pendingAction = { filePickerLauncher.launch(arrayOf("*/*")) }
                            showUnsavedChangesDialog = true
                        } else {
                            filePickerLauncher.launch(arrayOf("*/*"))
                        }
                    }
                )"""
content = content.replace(target_open, replacement_open)

target_fab = """                FloatingActionButton(
                    onClick = { viewModel.lockDatabase() },
                    containerColor = Color(0xFF0D47A1),
                    contentColor = Color.White,"""
replacement_fab = """                FloatingActionButton(
                    onClick = { 
                        if (hasUnsavedChanges) {
                            pendingAction = { viewModel.lockDatabase() }
                            showUnsavedChangesDialog = true
                        } else {
                            viewModel.lockDatabase()
                        }
                    },
                    containerColor = Color(0xFF0D47A1),
                    contentColor = Color.White,"""
content = content.replace(target_fab, replacement_fab)

with open('app/src/main/java/com/example/ui/VaultScreen.kt', 'w') as f:
    f.write(content)
print("Updated Open and FAB")
