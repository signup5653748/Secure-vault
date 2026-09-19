package com.example.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.DeleteOutline
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.viewmodel.KeePassViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    viewModel: KeePassViewModel,
    onNavigateBack: () -> Unit,
    onResetApp: () -> Unit = {}
) {
    val themeColor by viewModel.settings.themeColor.collectAsState()
    val textSizeMultiplier by viewModel.settings.textSizeMultiplier.collectAsState()
    val openFromFileManager by viewModel.settings.openFromFileManager.collectAsState()
    val lockOnBackground by viewModel.settings.lockOnBackground.collectAsState()
    val clipboardAutoClear by viewModel.settings.clipboardAutoClear.collectAsState()
    val enableBiometrics by viewModel.settings.enableBiometrics.collectAsState()
    var showResetConfirmationDialog by remember { mutableStateOf(false) }


    val colors = listOf("Blue", "Green", "Purple", "Orange", "Dynamic")

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Settings") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text("Theme Color", style = MaterialTheme.typography.titleMedium)
            
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                colors.forEach { color ->
                    FilterChip(
                        selected = themeColor == color,
                        onClick = { viewModel.settings.setThemeColor(color) },
                        label = { Text(color) }
                    )
                }
            }

            HorizontalDivider()

            Text("Text Size Multiplier: ${String.format("%.1f", textSizeMultiplier)}x", style = MaterialTheme.typography.titleMedium)
            Slider(
                value = textSizeMultiplier,
                onValueChange = { viewModel.settings.setTextSizeMultiplier(it) },
                valueRange = 0.5f..1.5f,
                steps = 9
            )

            HorizontalDivider()

            Row(
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
            HorizontalDivider()
            Text("Security & Auto-lock", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)

            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween,
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text("Lock on background", style = MaterialTheme.typography.titleMedium)
                    Text(
                        text = "Automatically lock secure when app goes to background.",
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
                    onCheckedChange = { viewModel.setEnableBiometrics(it) }
                )
            }

            HorizontalDivider()
            Text("Data & Privacy", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.error)

            Text(
                text = "Remove the current database association, wipe saved biometric unlock credentials from the Android Keystore, clear cached crash logs, and lock the vault.",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            OutlinedButton(
                onClick = { showResetConfirmationDialog = true },
                colors = ButtonDefaults.outlinedButtonColors(contentColor = MaterialTheme.colorScheme.error),
                modifier = Modifier.fillMaxWidth()
            ) {
                Icon(Icons.Default.DeleteOutline, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text("Forget Database & Clear Saved Credentials")
            }

            if (showResetConfirmationDialog) {
                AlertDialog(
                    onDismissRequest = { showResetConfirmationDialog = false },
                    icon = {
                        Icon(Icons.Default.DeleteOutline, contentDescription = null, tint = MaterialTheme.colorScheme.error)
                    },
                    title = { Text("Forget Database & Clear Data?") },
                    text = {
                        Text("This will remove the saved database URI, wipe stored biometric master password credentials, clear crash diagnostics, and lock the app.\n\nNote: Your .kdbx database file on disk will NOT be deleted.")
                    },
                    confirmButton = {
                        Button(
                            onClick = {
                                showResetConfirmationDialog = false
                                viewModel.forgetDatabaseAndClearData()
                                onResetApp()
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
                        ) {
                            Text("Clear & Lock")
                        }
                    },
                    dismissButton = {
                        TextButton(onClick = { showResetConfirmationDialog = false }) {
                            Text("Cancel")
                        }
                    }
                )
            }

        }
    }
}
