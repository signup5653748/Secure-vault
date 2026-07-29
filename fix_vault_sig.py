with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

import re

sig_pattern = r'fun VaultScreen\(\s*viewModel: KeePassViewModel,\s*onNavigateToView: \(\) -> Unit,\s*onNavigateToSettings: \(\) -> Unit,\s*onNavigateToCreate: \(\) -> Unit,\s*onNavigateToAbout: \(\) -> Unit,\s*onNavigateToAddEntry: \(\) -> Unit\s*\)'

sig_new = """fun VaultScreen(
    viewModel: KeePassViewModel,
    onNavigateToView: () -> Unit,
    onNavigateToSettings: () -> Unit,
    onNavigateToCreate: () -> Unit,
    onNavigateToAbout: () -> Unit,
    onNavigateToAddEntry: () -> Unit,
    onNavigateToTemplates: () -> Unit,
    onNavigateToAddNote: () -> Unit
)"""

content = re.sub(sig_pattern, sig_new, content)

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
    f.write(content)
