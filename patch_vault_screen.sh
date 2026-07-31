#!/bin/bash
sed -i 's/onNavigateToTemplates/onNavigateToEditGroup: () -> Unit = {},\n    onNavigateToEditEntry: () -> Unit = {},\n    onNavigateToTemplates/g' app/src/main/java/com/example/ui/VaultScreen.kt

sed -i 's/onEdit = debounced { viewModel.selectGroup(group) }/onEdit = debounced { viewModel.selectGroup(group); onNavigateToEditGroup() }/g' app/src/main/java/com/example/ui/VaultScreen.kt

sed -i 's/onEdit = debounced { viewModel.selectEntry(entry) }/onEdit = debounced { viewModel.selectEntry(entry); onNavigateToEditEntry() }/g' app/src/main/java/com/example/ui/VaultScreen.kt

