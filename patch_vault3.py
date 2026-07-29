import re

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'r') as f:
    content = f.read()

# Remove isProcessing
remove_isProcessing = """    var isProcessing by remember { mutableStateOf(false) }
    LaunchedEffect(Unit) { isProcessing = false } // Reset when returning to screen"""
content = content.replace(remove_isProcessing, "")

# Fix onDelete for group
group_delete_old = """                            onDelete = { 
                                if (!isProcessing) {
                                    isProcessing = true
                                    viewModel.deleteGroup(group)
                                    isProcessing = false // Reset immediately or let state handle it
                                }
                            }"""
group_delete_new = """                            onDelete = debounced { viewModel.deleteGroup(group) }"""
content = content.replace(group_delete_old, group_delete_new)

# Fix onDelete for entry (there are two)
entry_delete_old = """                            onDelete = { 
                                if (!isProcessing) {
                                    isProcessing = true
                                    viewModel.deleteEntry(entry)
                                    isProcessing = false
                                }
                            }"""
entry_delete_new = """                            onDelete = debounced { viewModel.deleteEntry(entry) }"""
content = content.replace(entry_delete_old, entry_delete_new)

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'w') as f:
    f.write(content)
