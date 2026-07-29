import re

with open('/app/applet/app/src/main/java/com/example/ui/AuthScreen.kt', 'r') as f:
    content = f.read()

# Add isLoading
state_old = """    val enableBiometrics by viewModel.settings.enableBiometrics.collectAsState()"""
state_new = """    val enableBiometrics by viewModel.settings.enableBiometrics.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()"""
content = content.replace(state_old, state_new)

# Add overlay when loading
overlay_old = """        if (error != null) {
            Spacer(modifier = Modifier.height(16.dp))
            Text(error!!, color = MaterialTheme.colorScheme.error)
        }
    }
}"""
overlay_new = """        if (error != null) {
            Spacer(modifier = Modifier.height(16.dp))
            Text(error!!, color = MaterialTheme.colorScheme.error)
        }
        
        if (isLoading) {
            Spacer(modifier = Modifier.height(32.dp))
            ColorfulLoadingIndicator()
            Spacer(modifier = Modifier.height(16.dp))
            Text("Decrypting Vault...", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.SemiBold)
        }
    }
}"""
content = content.replace(overlay_old, overlay_new)

# disable buttons when loading
buttons_old = """            Button(
                onClick = { viewModel.unlockDatabase(password) },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Unlock")
            }"""
buttons_new = """            Button(
                onClick = { viewModel.unlockDatabase(password) },
                modifier = Modifier.fillMaxWidth(),
                enabled = !isLoading && password.isNotEmpty()
            ) {
                Text("Unlock")
            }"""
content = content.replace(buttons_old, buttons_new)

with open('/app/applet/app/src/main/java/com/example/ui/AuthScreen.kt', 'w') as f:
    f.write(content)
