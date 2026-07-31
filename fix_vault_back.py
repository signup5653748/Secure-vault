import sys

with open('app/src/main/java/com/example/ui/VaultScreen.kt', 'r') as f:
    content = f.read()

target = """    BackHandler(enabled = !viewModel.isRootGroup()) {
        viewModel.navigateUp()
    }"""
replacement = """    BackHandler(enabled = true) {
        if (!viewModel.isRootGroup()) {
            viewModel.navigateUp()
        } else {
            if (hasUnsavedChanges) {
                pendingAction = { viewModel.lockDatabase() } // Exit essentially
                showUnsavedChangesDialog = true
            } else {
                viewModel.lockDatabase()
            }
        }
    }"""
content = content.replace(target, replacement)

with open('app/src/main/java/com/example/ui/VaultScreen.kt', 'w') as f:
    f.write(content)
print("Updated BackHandler")
