#!/bin/bash
sed -i 's/IconButton(onClick = onNavigateToSettings) {/IconButton(onClick = { viewModel.saveDatabase() }) {\n                            Icon(Icons.Default.Save, contentDescription = "Save")\n                        }\n                        IconButton(onClick = onNavigateToSettings) {/g' app/src/main/java/com/example/ui/VaultScreen.kt
