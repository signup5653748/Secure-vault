package com.example.ui

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.FolderOpen
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.viewmodel.KeePassViewModel
import androidx.compose.ui.platform.LocalContext
import androidx.compose.material.icons.filled.Fingerprint
import com.example.ui.BiometricHelper


@Composable
fun AuthScreen(viewModel: KeePassViewModel, onNavigateToCreate: () -> Unit) {
    val dbUri by viewModel.dbUri.collectAsState()
    val error by viewModel.error.collectAsState()
    val enableBiometrics by viewModel.settings.enableBiometrics.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val context = LocalContext.current
    
    var biometricPrompted by remember { mutableStateOf(false) }
    var hasSavedPass by remember { mutableStateOf(false) }

    LaunchedEffect(Unit) {
        val hasPass = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) {
            com.example.data.CryptoHelper.getPassword(context) != null
        }
        hasSavedPass = hasPass
    }

    LaunchedEffect(dbUri, enableBiometrics) {
        if (dbUri != null && enableBiometrics && !biometricPrompted) {
            val hasSaved = kotlinx.coroutines.withContext(kotlinx.coroutines.Dispatchers.IO) {
                com.example.data.CryptoHelper.getPassword(context) != null
            }
            if (hasSaved) {
                biometricPrompted = true
                BiometricHelper.showPrompt(
                    context = context,
                    onSuccess = { viewModel.unlockWithSavedPassword() },
                    onError = { }
                )
            }
        }
    }

    
    var password by remember { mutableStateOf("") }

    val filePickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.OpenDocument()
    ) { uri ->
        if (uri != null) {
            viewModel.importFile(uri)
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Icon(
            Icons.Default.Lock,
            contentDescription = null,
            modifier = Modifier.size(64.dp),
            tint = MaterialTheme.colorScheme.primary
        )
        Spacer(modifier = Modifier.height(16.dp))
        Text("Secure", fontSize = 32.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(32.dp))

        if (dbUri == null) {
            
            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = { filePickerLauncher.launch(arrayOf("*/*")) }
            ) {
                Icon(Icons.Default.FolderOpen, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text("Open Existing Secure")
            }
            Spacer(modifier = Modifier.height(8.dp))
            OutlinedButton(onClick = onNavigateToCreate) {
                Icon(Icons.Default.Add, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text("Create New Secure")
            }
        } else {
            Text(
                "Database selected",
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Spacer(modifier = Modifier.height(16.dp))
            OutlinedTextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Master Password") },
                visualTransformation = PasswordVisualTransformation(),
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )
            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = { viewModel.unlockDatabase(password) },
                modifier = Modifier.fillMaxWidth(),
                enabled = !isLoading && password.isNotEmpty()
            ) {
                Text("Unlock")
            }
            if (enableBiometrics && hasSavedPass) {
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
            }
            Spacer(modifier = Modifier.height(16.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                TextButton(
                    onClick = { filePickerLauncher.launch(arrayOf("*/*")) }
                ) {
                    Text("Select different")
                }
                TextButton(
                    onClick = onNavigateToCreate
                ) {
                    Text("Create new")
                }
            }
        }

        if (error != null) {
            Spacer(modifier = Modifier.height(16.dp))
            Text(error!!, color = MaterialTheme.colorScheme.error)
        }
        
        if (isLoading) {
            Spacer(modifier = Modifier.height(32.dp))
            ColorfulLoadingIndicator()
            Spacer(modifier = Modifier.height(16.dp))
            Text("Decrypting Secure...", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.SemiBold)
        }
    }
}
