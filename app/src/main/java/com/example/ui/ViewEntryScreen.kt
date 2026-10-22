package com.example.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.combinedClickable
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import kotlinx.coroutines.launch
import androidx.compose.material.icons.filled.Label
import androidx.compose.material.icons.filled.Attachment
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.automirrored.filled.*
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
import androidx.compose.foundation.Canvas
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.platform.testTag
import com.example.data.OtpParser
import com.example.data.OtpGenerator

@OptIn(ExperimentalMaterial3Api::class, ExperimentalFoundationApi::class)
@Composable
fun ViewEntryScreen(
    viewModel: KeePassViewModel,
    onNavigateBack: () -> Unit,
    onNavigateToEdit: () -> Unit
) {
    val currentEntry by viewModel.currentEntry.collectAsState()
    val clipboardManager: ClipboardManager = LocalClipboardManager.current
    val context = androidx.compose.ui.platform.LocalContext.current
    var passwordVisible by remember { mutableStateOf(false) }

    val snackbarHostState = remember { SnackbarHostState() }
    val scope = rememberCoroutineScope()
    var showMoveDialog by remember { mutableStateOf(false) }

    if (showMoveDialog && currentEntry != null) {
        val entry = currentEntry!!
        val destinations = remember(entry) {
            viewModel.getAvailableGroupDestinationsForEntry(entry)
        }
        val title = entry[BasicField.Title]?.content ?: "Entry"
        MoveItemDialog(
            title = "Move Entry",
            itemName = title,
            destinations = destinations,
            onDismiss = { showMoveDialog = false },
            onConfirmMove = { targetGroupUuid ->
                viewModel.moveEntry(entry, targetGroupUuid) { success, msg ->
                    scope.launch {
                        snackbarHostState.showSnackbar(msg)
                    }
                }
                showMoveDialog = false
            }
        )
    }

    Scaffold(
        snackbarHost = { SnackbarHost(snackbarHostState) },
        topBar = {
            var isEditing by remember { mutableStateOf(false) }
            TopAppBar(
                title = { Text("") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { showMoveDialog = true }) {
                        Icon(Icons.AutoMirrored.Filled.DriveFileMove, contentDescription = "Move Entry")
                    }
                    IconButton(onClick = {
                        if (!isEditing) {
                            isEditing = true
                            onNavigateToEdit()
                            isEditing = false
                        }
                    }) {
                        Icon(Icons.Default.Edit, contentDescription = "Edit")
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
            
            Spacer(modifier = Modifier.height(32.dp))

            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
            ) {
                Column {


                    if (entry.fields.containsKey(BasicField.UserName()) && !(entry[BasicField.UserName]?.content ?: "").isNullOrEmpty()) {
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
                        IconButton(onClick = { 
                            if (!passwordVisible) {
                                val canAuth = BiometricHelper.canAuthenticate(context) ||
                                        BiometricHelper.canAuthenticateWithDeviceCredential(context)
                                if (canAuth) {
                                    BiometricHelper.showPrompt(
                                        context = context,
                                        title = "View Password",
                                        subtitle = "Verify your fingerprint to view password",
                                        onSuccess = { passwordVisible = true },
                                        onError = {
                                            // Fallback to reveal if cancelled or failed
                                            passwordVisible = true
                                        }
                                    )
                                } else {
                                    passwordVisible = true
                                }
                            } else {
                                passwordVisible = false
                            }
                        }) {
                            Icon(
                                if (passwordVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility,
                                contentDescription = "Toggle Visibility"
                            )
                        }
                        IconButton(onClick = { 
                            val pwd = entry[BasicField.Password]?.content ?: ""
                            clipboardManager.setText(AnnotatedString(pwd))
                            android.widget.Toast.makeText(context, "Password copied to clipboard", android.widget.Toast.LENGTH_SHORT).show()
                        }) {
                            Icon(Icons.Default.ContentCopy, contentDescription = "Copy Password")
                        }
                    }
                }
            }

            // TOTP Card
            val otpValue = entry.fields.entries.find { it.key.equals("otp", ignoreCase = true) }?.value?.content
            if (!otpValue.isNullOrBlank()) {
                var totpData by remember(otpValue) { mutableStateOf(viewModel.generateTotpCode(otpValue)) }

                LaunchedEffect(otpValue) {
                    while (true) {
                        kotlinx.coroutines.delay(1000)
                        totpData = viewModel.generateTotpCode(otpValue)
                    }
                }

                Spacer(modifier = Modifier.height(24.dp))
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .testTag("otp_card"),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(Icons.Default.QrCode, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                        Spacer(modifier = Modifier.width(16.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(text = "Authentication Code", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            Text(
                                text = totpData?.first ?: "••••••",
                                fontSize = 24.sp,
                                fontWeight = FontWeight.Bold,
                                fontFamily = FontFamily.Monospace,
                                letterSpacing = 4.sp,
                                color = MaterialTheme.colorScheme.onSurface,
                                modifier = Modifier.testTag("otp_code_text")
                            )
                        }
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text(text = "${totpData?.second ?: 30}s", fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        IconButton(
                            onClick = { 
                                totpData?.first?.let { code ->
                                    clipboardManager.setText(AnnotatedString(code))
                                    android.widget.Toast.makeText(context, "OTP copied", android.widget.Toast.LENGTH_SHORT).show()
                                }
                            },
                            modifier = Modifier.testTag("copy_otp_button")
                        ) {
                            Icon(Icons.Default.ContentCopy, contentDescription = "Copy OTP")
                        }
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Custom fields
            val basicKeys = setOf(BasicField.Title(), BasicField.UserName(), BasicField.Password(), BasicField.Url(), BasicField.Notes())
            val customFields = entry.fields.entries.filter { 
                it.key !in basicKeys && it.key != "Notes" && it.key != "Title" && it.key != "UserName" && it.key != "URL" && it.key != "Password" && !it.key.equals("otp", ignoreCase = true)
            }
            
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
                    androidx.compose.foundation.text.selection.SelectionContainer {
                        Text(
                            text = (entry[BasicField.Notes]?.content ?: ""),
                            modifier = Modifier.padding(16.dp),
                            fontSize = 16.sp
                        )
                    }
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
                            leadingIcon = { Icon(Icons.AutoMirrored.Filled.Label, contentDescription = null, modifier = Modifier.size(16.dp)) }
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
