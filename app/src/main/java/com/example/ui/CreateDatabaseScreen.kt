package com.example.ui

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import com.example.viewmodel.KeePassViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CreateDatabaseScreen(
    viewModel: KeePassViewModel,
    onNavigateBack: () -> Unit
) {
    var databaseName by remember { mutableStateOf("secure") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    var errorMsg by remember { mutableStateOf<String?>(null) }
    var isCreating by remember { mutableStateOf(false) }

    val createDocumentLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.CreateDocument("application/octet-stream")
    ) { uri: Uri? ->
        if (uri != null) {
            isCreating = true
            viewModel.createDatabase(uri, password) { success, errMsg ->
                isCreating = false
                if (success) {
                    onNavigateBack() // Go back to auth screen to unlock it
                } else {
                    errorMsg = errMsg ?: "Failed to create database"
                }
            }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Create New Database") },
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
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            Text(
                "Create a new KeePass database (KDBX). " +
                "You will be asked to choose where to save the file.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )

            OutlinedTextField(
                value = databaseName,
                onValueChange = { databaseName = it; errorMsg = null },
                label = { Text("Database Name") },
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )

            OutlinedTextField(
                value = password,
                onValueChange = { password = it; errorMsg = null },
                label = { Text("Master Password") },
                visualTransformation = PasswordVisualTransformation(),
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )

            OutlinedTextField(
                value = confirmPassword,
                onValueChange = { confirmPassword = it; errorMsg = null },
                label = { Text("Confirm Password") },
                visualTransformation = PasswordVisualTransformation(),
                modifier = Modifier.fillMaxWidth(),
                singleLine = true
            )

            if (errorMsg != null) {
                Text(errorMsg!!, color = MaterialTheme.colorScheme.error)
            }

            Button(
                onClick = {
                    if (databaseName.isEmpty()) {
                        errorMsg = "Database name cannot be empty"
                    } else if (password.isEmpty()) {
                        errorMsg = "Password cannot be empty"
                    } else if (password != confirmPassword) {
                        errorMsg = "Passwords do not match"
                    } else {
                        // Start SAF picker
                        val fileName = if (databaseName.endsWith(".kdbx", ignoreCase = true)) databaseName else "$databaseName.kdbx"
                        createDocumentLauncher.launch(fileName)
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = !isCreating
            ) {
                if (isCreating) {
                    CircularProgressIndicator(modifier = Modifier.size(24.dp))
                } else {
                    Text("Create and Save")
                }
            }
        }
    }
}
