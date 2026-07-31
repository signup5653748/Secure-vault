#!/bin/bash
sed -i 's/onClick = debounced { viewModel.selectGroup(group) },/onClick = debounced { viewModel.selectGroup(group) },\n                            onEdit = debounced { viewModel.selectGroup(group); onNavigateToEditGroup() },/g' app/src/main/java/com/example/ui/VaultScreen.kt

sed -i 's/onClick = debounced { /onClick = debounced { /g' app/src/main/java/com/example/ui/VaultScreen.kt

