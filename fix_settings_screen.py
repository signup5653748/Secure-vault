import re

with open('/app/applet/app/src/main/java/com/example/ui/SettingsScreen.kt', 'r') as f:
    content = f.read()

new_imports = """import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
"""

content = content.replace('import androidx.compose.foundation.layout.*', 'import androidx.compose.foundation.layout.*\n' + new_imports)

# Replace Column to add verticalScroll
content = content.replace("""        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp),""", """        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
                .verticalScroll(rememberScrollState()),""")

new_state_vars = """    val openFromFileManager by viewModel.settings.openFromFileManager.collectAsState()
    val lockOnBackground by viewModel.settings.lockOnBackground.collectAsState()
    val clipboardAutoClear by viewModel.settings.clipboardAutoClear.collectAsState()
    val enableBiometrics by viewModel.settings.enableBiometrics.collectAsState()
"""
content = content.replace("    val openFromFileManager by viewModel.settings.openFromFileManager.collectAsState()", new_state_vars)

new_settings_ui = """            Divider()
            Text("Security & Auto-lock", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)

            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("Lock on background", style = MaterialTheme.typography.titleMedium)
                    Text(
                        text = "Automatically lock vault when app goes to background.",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Switch(
                    checked = lockOnBackground,
                    onCheckedChange = { viewModel.settings.setLockOnBackground(it) }
                )
            }
            
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("Clipboard auto-clear", style = MaterialTheme.typography.titleMedium)
                    Text(
                        text = "Clear clipboard when app is locked.",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Switch(
                    checked = clipboardAutoClear,
                    onCheckedChange = { viewModel.settings.setClipboardAutoClear(it) }
                )
            }
            
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("Fingerprint / Biometrics", style = MaterialTheme.typography.titleMedium)
                    Text(
                        text = "Use biometric authentication to unlock.",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Switch(
                    checked = enableBiometrics,
                    onCheckedChange = { viewModel.settings.setEnableBiometrics(it) }
                )
            }
"""

content = content.replace("""            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("Open KDBX from File Manager", style = MaterialTheme.typography.titleMedium)
                    Text(
                        text = "Allows opening databases directly from the file manager.",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Switch(
                    checked = openFromFileManager,
                    onCheckedChange = { viewModel.settings.setOpenFromFileManager(it) }
                )
            }
        }""", """            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("Open KDBX from File Manager", style = MaterialTheme.typography.titleMedium)
                    Text(
                        text = "Allows opening databases directly from the file manager.",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
                Switch(
                    checked = openFromFileManager,
                    onCheckedChange = { viewModel.settings.setOpenFromFileManager(it) }
                )
            }
""" + new_settings_ui + "\n        }")

# Re-use horizontal divider logic
content = content.replace("Divider()", "HorizontalDivider()")

with open('/app/applet/app/src/main/java/com/example/ui/SettingsScreen.kt', 'w') as f:
    f.write(content)

