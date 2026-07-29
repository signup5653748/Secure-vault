import re

with open('/app/applet/app/src/main/java/com/example/ui/ViewEntryScreen.kt', 'r') as f:
    content = f.read()

top_bar_old = """            TopAppBar(
                title = { Text((currentEntry?.get(BasicField.Title)?.content ?: "Entry")) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )"""
top_bar_new = """            var isEditing by remember { mutableStateOf(false) }
            TopAppBar(
                title = { Text((currentEntry?.get(BasicField.Title)?.content ?: "Entry")) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = {
                        if (!isEditing) {
                            isEditing = true
                            onNavigateToEdit()
                            isEditing = false
                        }
                    }) {
                        Icon(Icons.Default.Edit, contentDescription = "Edit")
                    }
                }
            )"""
content = content.replace(top_bar_old, top_bar_new)

# Also need to add onNavigateToEdit to the ViewEntryScreen arguments
args_old = """fun ViewEntryScreen(
    viewModel: KeePassViewModel,
    onNavigateBack: () -> Unit
) {"""
args_new = """fun ViewEntryScreen(
    viewModel: KeePassViewModel,
    onNavigateBack: () -> Unit,
    onNavigateToEdit: () -> Unit
) {"""
content = content.replace(args_old, args_new)

with open('/app/applet/app/src/main/java/com/example/ui/ViewEntryScreen.kt', 'w') as f:
    f.write(content)
