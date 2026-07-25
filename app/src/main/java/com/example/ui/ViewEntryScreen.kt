package com.example.ui

import androidx.compose.foundation.layout.*
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
import java.text.SimpleDateFormat
import java.util.*

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
                color = MaterialTheme.colorScheme.surfaceVariant,
                modifier = Modifier.size(80.dp)
            ) {
                Icon(
                    Icons.Default.Lock,
                    contentDescription = null,
                    modifier = Modifier.padding(16.dp),
                    tint = MaterialTheme.colorScheme.onSurfaceVariant
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
