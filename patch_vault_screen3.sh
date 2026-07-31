#!/bin/bash
sed -i 's/onDelete = debounced { viewModel.deleteEntry(entry) }/onEdit = debounced { viewModel.selectEntry(entry); onNavigateToEditEntry() },\n                            onDelete = debounced { viewModel.deleteEntry(entry) }/g' app/src/main/java/com/example/ui/VaultScreen.kt
