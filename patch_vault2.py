import re

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'r') as f:
    content = f.read()

# Add import
import_old = "import androidx.compose.runtime.*"
import_new = "import androidx.compose.runtime.*\nimport com.example.ui.debounced"
if "import com.example.ui.debounced" not in content:
    content = content.replace(import_old, import_new)

# Patch entry click to use debounced
entry_click_old = """                            onClick = { 
                                if (!isProcessing) {
                                    isProcessing = true
                                    viewModel.selectEntry(entry)
                                    onNavigateToView()
                                }
                            },"""
entry_click_new = """                            onClick = debounced { 
                                viewModel.selectEntry(entry)
                                onNavigateToView()
                            },"""
content = content.replace(entry_click_old, entry_click_new)

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'w') as f:
    f.write(content)

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'r') as f:
    content = f.read()

group_click_old = """                            onClick = { 
                                if (!isProcessing) {
                                    viewModel.selectGroup(group)
                                }
                            },"""
group_click_new = """                            onClick = debounced { viewModel.selectGroup(group) },"""
content = content.replace(group_click_old, group_click_new)

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'w') as f:
    f.write(content)
