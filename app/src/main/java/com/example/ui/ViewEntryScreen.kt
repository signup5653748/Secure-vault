package com.example.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.filled.Label
import androidx.compose.material.icons.filled.Attachment
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.ClipboardManager
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.viewmodel.KeePassViewModel
import app.keemobile.kotpass.constants.BasicField
import app.keemobile.kotpass.models.Entry
import app.keemobile.kotpass.models.EntryValue

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ViewEntryScreen(
    viewModel: KeePassViewModel,
    onNavigateBack: () -> Unit
) {
    val currentEntry by viewModel.currentEntry.collectAsState()
    val clipboardManager: ClipboardManager = LocalClipboardManager.current
    var passwordVisible by remember { mutableStateOf(false) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text((currentEntry?.get(BasicField.Title)?.content ?: "Entry")) },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { paddingValues ->
        if (currentEntry == null) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
            return@Scaffold
        }
        val entry = currentEntry!!
        val iconColor = parseColor(entry.customData["ThemeColor"]?.value)
        val iconVector = parseIcon(entry.icon.name)

        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(modifier = Modifier.height(24.dp))
            
            Surface(
                shape = MaterialTheme.shapes.large,
                color = iconColor.copy(alpha = 0.2f),
                modifier = Modifier.size(80.dp)
            ) {
                Icon(
                    iconVector,
                    contentDescription = null,
                    modifier = Modifier.padding(16.dp),
                    tint = iconColor
                )
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Text(text = (entry[BasicField.Title]?.content ?: "") ?: "", fontWeight = FontWeight.Bold, fontSize = 24.sp)
            Text(text = "Personal Credentials", fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)

            Spacer(modifier = Modifier.height(32.dp))

            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
            ) {
                Column {
                    if (!(entry[BasicField.Url]?.content ?: "").isNullOrEmpty()) {
                        ViewFieldRow(
                            icon = Icons.Default.Link,
                            text = (entry[BasicField.Url]?.content ?: ""),
                            onCopy = { clipboardManager.setText(AnnotatedString((entry[BasicField.Url]?.content ?: ""))) }
                        )
                        HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
                    }

                    if (!(entry[BasicField.UserName]?.content ?: "").isNullOrEmpty()) {
                        ViewFieldRow(
                            icon = Icons.Default.Person,
                            text = (entry[BasicField.UserName]?.content ?: ""),
                            onCopy = { clipboardManager.setText(AnnotatedString((entry[BasicField.UserName]?.content ?: ""))) }
                        )
                        HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
                    }
                    
                    // Password Row
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            Icons.Default.VpnKey,
                            contentDescription = null,
                            tint = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Spacer(modifier = Modifier.width(16.dp))
                        Text(
                            text = if (passwordVisible) (entry[BasicField.Password]?.content ?: "") else "••••••••••••",
                            modifier = Modifier.weight(1f),
                            fontSize = 16.sp
                        )
                        IconButton(onClick = { passwordVisible = !passwordVisible }) {
                            Icon(
                                if (passwordVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility,
                                contentDescription = "Toggle Visibility"
                            )
                        }
                        IconButton(onClick = { clipboardManager.setText(AnnotatedString((entry[BasicField.Password]?.content ?: ""))) }) {
                            Icon(Icons.Default.ContentCopy, contentDescription = "Copy Password")
                        }
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Custom fields
            val basicKeys = setOf("Title", "UserName", "Password", "URL", "Notes")
            val customFields = entry.fields.entries.filter { it.key !in basicKeys }
            
            if (customFields.isNotEmpty()) {
                Text(
                    text = "Custom Fields",
                    fontWeight = FontWeight.Medium,
                    modifier = Modifier.align(Alignment.Start),
                    color = MaterialTheme.colorScheme.primary
                )
                Spacer(modifier = Modifier.height(8.dp))
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                ) {
                    Column {
                        customFields.forEachIndexed { index, (key, value) ->
                            var isVisible by remember { mutableStateOf(false) }
                            val isHidden = value is EntryValue.Encrypted
                            val displayValue = if (isHidden && !isVisible) "••••••••" else value.content
                            
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(16.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Column(modifier = Modifier.weight(1f)) {
                                    Text(text = key, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                                    Text(text = displayValue, fontSize = 16.sp)
                                }
                                if (isHidden) {
                                    IconButton(onClick = { isVisible = !isVisible }) {
                                        Icon(if (isVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, "Toggle")
                                    }
                                }
                                val showCopyButton = entry.customData["ShowCopyButton_${key}"]?.value?.toBooleanStrictOrNull() ?: true
                                if (showCopyButton) {
                                    IconButton(onClick = { clipboardManager.setText(AnnotatedString(value.content)) }) {
                                        Icon(Icons.Default.ContentCopy, contentDescription = "Copy")
                                    }
                                }
                            }
                            if (index < customFields.size - 1) {
                                HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
                            }
                        }
                    }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }
            
            if (!(entry[BasicField.Notes]?.content ?: "").isNullOrEmpty()) {
                Text(
                    text = "Notes",
                    fontWeight = FontWeight.Medium,
                    modifier = Modifier.align(Alignment.Start),
                    color = MaterialTheme.colorScheme.primary
                )
                Spacer(modifier = Modifier.height(8.dp))
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                ) {
                    Text(
                        text = (entry[BasicField.Notes]?.content ?: ""),
                        modifier = Modifier.padding(16.dp),
                        fontSize = 16.sp
                    )
                }
            }

            if (entry.tags.isNotEmpty()) {
                Spacer(modifier = Modifier.height(24.dp))
                Text(
                    text = "Tags",
                    fontWeight = FontWeight.Medium,
                    modifier = Modifier.align(Alignment.Start),
                    color = MaterialTheme.colorScheme.primary
                )
                Spacer(modifier = Modifier.height(8.dp))
                LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    items(entry.tags) { tag ->
                        AssistChip(
                            onClick = { },
                            label = { Text(tag) },
                            leadingIcon = { Icon(Icons.Default.Label, contentDescription = null, modifier = Modifier.size(16.dp)) }
                        )
                    }
                }
            }
            
            if (entry.binaries.isNotEmpty()) {
                Spacer(modifier = Modifier.height(24.dp))
                Text(
                    text = "Attachments",
                    fontWeight = FontWeight.Medium,
                    modifier = Modifier.align(Alignment.Start),
                    color = MaterialTheme.colorScheme.primary
                )
                Spacer(modifier = Modifier.height(8.dp))
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                ) {
                    Column {
                        entry.binaries.forEachIndexed { index, binaryRef ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(16.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Icon(
                                    Icons.Default.Attachment,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                                Spacer(modifier = Modifier.width(16.dp))
                                Text(text = binaryRef.name, modifier = Modifier.weight(1f), fontSize = 16.sp, maxLines = 1)
                            }
                            if (index < entry.binaries.size - 1) {
                                HorizontalDivider(color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f))
                            }
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}

@Composable
fun ViewFieldRow(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String, onCopy: () -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(
            icon,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Spacer(modifier = Modifier.width(16.dp))
        Text(text = text, modifier = Modifier.weight(1f), fontSize = 16.sp)
        IconButton(onClick = onCopy) {
            Icon(Icons.Default.ContentCopy, contentDescription = "Copy")
        }
    }
}
