import re

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'r') as f:
    content = f.read()

var_old = """    var showMenu by remember { mutableStateOf(false) }"""
var_new = """    var showMenu by remember { mutableStateOf(false) }
    var isProcessing by remember { mutableStateOf(false) }
    LaunchedEffect(Unit) { isProcessing = false } // Reset when returning to screen"""
content = content.replace(var_old, var_new)

# Patch group click
group_click_old = """                            onClick = { viewModel.selectGroup(group) },"""
group_click_new = """                            onClick = { 
                                if (!isProcessing) {
                                    viewModel.selectGroup(group)
                                }
                            },"""
content = content.replace(group_click_old, group_click_new)

# Patch group delete
group_delete_old = """                            onDelete = { viewModel.deleteGroup(group) }"""
group_delete_new = """                            onDelete = { 
                                if (!isProcessing) {
                                    isProcessing = true
                                    viewModel.deleteGroup(group)
                                    isProcessing = false // Reset immediately or let state handle it
                                }
                            }"""
content = content.replace(group_delete_old, group_delete_new)

# Patch entry click
entry_click_old = """                            onClick = { 
                                viewModel.selectEntry(entry)
                                onNavigateToView()
                            },"""
entry_click_new = """                            onClick = { 
                                if (!isProcessing) {
                                    isProcessing = true
                                    viewModel.selectEntry(entry)
                                    onNavigateToView()
                                }
                            },"""
content = content.replace(entry_click_old, entry_click_new)

# Patch entry delete
entry_delete_old = """                            onDelete = { viewModel.deleteEntry(entry) }"""
entry_delete_new = """                            onDelete = { 
                                if (!isProcessing) {
                                    isProcessing = true
                                    viewModel.deleteEntry(entry)
                                    isProcessing = false
                                }
                            }"""
content = content.replace(entry_delete_old, entry_delete_new)

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'w') as f:
    f.write(content)
