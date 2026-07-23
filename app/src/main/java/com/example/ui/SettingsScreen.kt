package com.example.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.viewmodel.KeePassViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    viewModel: KeePassViewModel,
    onNavigateBack: () -> Unit
) {
    val themeColor by viewModel.settings.themeColor.collectAsState()
    val textSizeMultiplier by viewModel.settings.textSizeMultiplier.collectAsState()
    val openFromFileManager by viewModel.settings.openFromFileManager.collectAsState()

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
                .padding(16.dp),
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

            Divider()

            Text("Text Size Multiplier: ${String.format("%.1f", textSizeMultiplier)}x", style = MaterialTheme.typography.titleMedium)
            Slider(
                value = textSizeMultiplier,
                onValueChange = { viewModel.settings.setTextSizeMultiplier(it) },
                valueRange = 0.5f..1.5f,
                steps = 9
            )

            Divider()

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
        }
    }
}
