import re

with open('/app/applet/app/src/main/java/com/example/ui/AuthScreen.kt', 'r') as f:
    content = f.read()

new_imports = """import androidx.compose.ui.platform.LocalContext
import androidx.compose.material.icons.filled.Fingerprint
import com.example.ui.BiometricHelper
"""

content = content.replace("import com.example.viewmodel.KeePassViewModel", "import com.example.viewmodel.KeePassViewModel\n" + new_imports)

new_state = """    val dbUri by viewModel.dbUri.collectAsState()
    val error by viewModel.error.collectAsState()
    val enableBiometrics by viewModel.settings.enableBiometrics.collectAsState()
    val context = LocalContext.current
    
    var biometricPrompted by remember { mutableStateOf(false) }

    LaunchedEffect(dbUri, enableBiometrics) {
        if (dbUri != null && enableBiometrics && !biometricPrompted) {
            val hasSavedPass = com.example.data.CryptoHelper.getPassword(context) != null
            if (hasSavedPass) {
                biometricPrompted = true
                BiometricHelper.showPrompt(
                    context = context,
                    onSuccess = { viewModel.unlockWithSavedPassword() },
                    onError = { }
                )
            }
        }
    }
"""

content = content.replace("""    val dbUri by viewModel.dbUri.collectAsState()
    val error by viewModel.error.collectAsState()""", new_state)

new_buttons = """            Button(
                onClick = { viewModel.unlockDatabase(password) },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Unlock")
            }
            if (enableBiometrics && com.example.data.CryptoHelper.getPassword(context) != null) {
                Spacer(modifier = Modifier.height(8.dp))
                OutlinedButton(
                    onClick = {
                        BiometricHelper.showPrompt(
                            context = context,
                            onSuccess = { viewModel.unlockWithSavedPassword() },
                            onError = { }
                        )
                    },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Icon(Icons.Default.Fingerprint, contentDescription = null)
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Unlock with Biometrics")
                }
            }"""

content = content.replace("""            Button(
                onClick = { viewModel.unlockDatabase(password) },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Unlock")
            }""", new_buttons)

with open('/app/applet/app/src/main/java/com/example/ui/AuthScreen.kt', 'w') as f:
    f.write(content)

