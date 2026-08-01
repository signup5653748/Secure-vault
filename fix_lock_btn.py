import re

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

target = """                    actions = {
                        IconButton(onClick = { viewModel.saveDatabase() }) {"""

replacement = """                    actions = {
                        IconButton(onClick = {
                            if (hasUnsavedChanges) {
                                pendingAction = { viewModel.lockDatabase() }
                                showUnsavedChangesDialog = true
                            } else {
                                viewModel.lockDatabase()
                            }
                        }) {
                            Icon(Icons.Default.Lock, contentDescription = "Lock")
                        }
                        IconButton(onClick = { viewModel.saveDatabase() }) {"""

content = content.replace(target, replacement)

target2 = """            if (database != null) {
                FloatingActionButton(
                    onClick = {
                        if (hasUnsavedChanges) {
                            pendingAction = { viewModel.lockDatabase() }
                            showUnsavedChangesDialog = true
                        } else {
                            viewModel.lockDatabase()
                        }
                    },
                    containerColor = Color(0xFF0D47A1),
                    contentColor = Color.White,
                    shape = androidx.compose.foundation.shape.RoundedCornerShape(16.dp),
                    modifier = Modifier
                        .align(Alignment.BottomStart)
                        .padding(start = 16.dp, bottom = 16.dp)
                ) {
                    Icon(Icons.Default.Lock, contentDescription = "Lock")
                }
            }"""

content = content.replace(target2, "")

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
    f.write(content)
print("fixed lock btn")
