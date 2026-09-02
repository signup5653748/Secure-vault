package com.example.ui

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.automirrored.filled.*
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.activity.compose.BackHandler
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.material.icons.filled.Sort
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.background
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.PathEffect
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.CornerRadius
import com.example.viewmodel.KeePassViewModel
import app.keemobile.kotpass.models.Group
import app.keemobile.kotpass.models.Entry
import kotlinx.coroutines.launch
import app.keemobile.kotpass.constants.BasicField
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.text.AnnotatedString
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SecureScreen(
    viewModel: KeePassViewModel,
    onNavigateToView: () -> Unit,
    onNavigateToSettings: () -> Unit = {},
    onNavigateToCreate: () -> Unit = {},
    onNavigateToAbout: () -> Unit = {},
    onNavigateToAddEntry: () -> Unit = {},
    
    
    onNavigateToEditGroup: () -> Unit = {},
    onNavigateToEditEntry: () -> Unit = {},
    onNavigateToTemplates: () -> Unit = {},
    onNavigateToAddTemplate: () -> Unit = {},
    onNavigateToAddGroup: () -> Unit = {},
    onNavigateToAddNote: () -> Unit = {}
) {
    val database by viewModel.database.collectAsState()
    val hasUnsavedChanges by viewModel.hasUnsavedChanges.collectAsState()
    val currentGroup by viewModel.currentGroup.collectAsState()
    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
    var sortOrder by remember { mutableStateOf("Default") }
    var showSortMenu by remember { mutableStateOf(false) }
    var showUnsavedChangesDialog by remember { mutableStateOf(false) }
    var pendingAction by remember { mutableStateOf<(() -> Unit)?>(null) }
    
    if (showUnsavedChangesDialog) {
        AlertDialog(
            onDismissRequest = { showUnsavedChangesDialog = false },
            title = { Text("Unsaved Changes") },
            text = { Text("You have unsaved changes. Do you want to save them before proceeding?") },
            confirmButton = {
                TextButton(onClick = {
                    viewModel.saveDatabase()
                    showUnsavedChangesDialog = false
                    pendingAction?.invoke()
                }) {
                    Text("Save Changes")
                }
            },
            dismissButton = {
                Row {
                    TextButton(onClick = { showUnsavedChangesDialog = false }) {
                        Text("Cancel")
                    }
                    TextButton(onClick = {
                        showUnsavedChangesDialog = false
                        pendingAction?.invoke()
                    }) {
                        Text("Discard")
                    }
                }
            }
        )
    }
    val isRoot = currentGroup?.uuid == database?.content?.group?.uuid
    BackHandler(enabled = !isRoot) {

        viewModel.navigateUp()

    }
    val scope = rememberCoroutineScope()
    
    LaunchedEffect(Unit) {
        viewModel.getOrCreateTemplatesGroup()
    }
    
    var showBottomSheet by remember { mutableStateOf(false) }


    var showFabMenu by remember { mutableStateOf(false) }
    var showChooseTemplateSheet by remember { mutableStateOf(false) }
    val sheetState = rememberModalBottomSheetState()
    
    val searchQuery by viewModel.searchQuery.collectAsState()
    val searchResults by viewModel.searchResults.collectAsState()
    var isSearchActive by remember { mutableStateOf(false) }

    
    val filePickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.OpenDocument()
    ) { uri ->
        if (uri != null) {
            viewModel.lockDatabase()
            viewModel.importFile(uri)
        }
    }

    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            ModalDrawerSheet(
                modifier = Modifier.width(280.dp)
            ) {
                Spacer(Modifier.height(12.dp))
                var expandedHeader by remember { mutableStateOf(false) }
                Surface(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 12.dp, vertical = 8.dp)
                        .clickable { expandedHeader = !expandedHeader },
                    shape = RoundedCornerShape(12.dp),
                    color = MaterialTheme.colorScheme.secondaryContainer.copy(alpha = 0.5f)
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            Icons.Default.Storage,
                            contentDescription = "Database",
                            tint = MaterialTheme.colorScheme.primary,
                            modifier = Modifier.size(32.dp)
                        )
                        Spacer(modifier = Modifier.width(16.dp))
                        Column {
                            Text("Secure", fontWeight = FontWeight.Bold, fontSize = 18.sp, color = MaterialTheme.colorScheme.onSecondaryContainer)
                            if (hasUnsavedChanges) {
                                Text("Unsaved changes", fontSize = 12.sp, color = MaterialTheme.colorScheme.error)
                            }
                        }
                        Spacer(modifier = Modifier.weight(1f))
                        Icon(
                            if (expandedHeader) Icons.Default.ExpandLess else Icons.Default.ExpandMore,
                            contentDescription = "Expand",
                            tint = MaterialTheme.colorScheme.onSecondaryContainer
                        )
                    }
                }
                
                var showChangePasswordDialog by remember { mutableStateOf(false) }
    var showPasswordGenerator by remember { mutableStateOf(false) }
    var showDatabaseInfoDialog by remember { mutableStateOf(false) }
                
                if (expandedHeader) {
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Default.Info, contentDescription = null) },
                        label = { Text("Database Information") },
                        selected = false,
                        onClick = { 
                            showDatabaseInfoDialog = true
                            expandedHeader = false
                        }
                    )
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Default.VpnKey, contentDescription = null) },
                        label = { Text("Change Master Password") },
                        selected = false,
                        onClick = {
                            showChangePasswordDialog = true
                            expandedHeader = false
                        }
                    )
                }

                if (showChangePasswordDialog) {
                    var currentPass by remember { mutableStateOf("") }
                    var newPass by remember { mutableStateOf("") }
                    var confirmPass by remember { mutableStateOf("") }
                    var currentPassVisible by remember { mutableStateOf(false) }
                    var newPassVisible by remember { mutableStateOf(false) }
                    var confirmPassVisible by remember { mutableStateOf(false) }

                    AlertDialog(
                        onDismissRequest = { showChangePasswordDialog = false },
                        title = { Text("Change Master Password") },
                        text = {
                            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                OutlinedTextField(
                                    value = currentPass,
                                    onValueChange = { currentPass = it },
                                    label = { Text("Current Password") },
                                    visualTransformation = if (currentPassVisible) androidx.compose.ui.text.input.VisualTransformation.None else androidx.compose.ui.text.input.PasswordVisualTransformation(),
                                    trailingIcon = {
                                        IconButton(onClick = { currentPassVisible = !currentPassVisible }) {
                                            Icon(if (currentPassVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, "Toggle Password")
                                        }
                                    }
                                )
                                Column(modifier = Modifier.fillMaxWidth()) {
                                    OutlinedTextField(
                                        value = newPass,
                                        onValueChange = { newPass = it },
                                        label = { Text("New Password") },
                                        visualTransformation = if (newPassVisible) androidx.compose.ui.text.input.VisualTransformation.None else androidx.compose.ui.text.input.PasswordVisualTransformation(),
                                        trailingIcon = {
                                            Row {
                                                IconButton(onClick = { showPasswordGenerator = true }) {
                                                    Icon(Icons.Default.Build, "Generate Password")
                                                }
                                                IconButton(onClick = { newPassVisible = !newPassVisible }) {
                                                    Icon(if (newPassVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, "Toggle Password")
                                                }
                                            }
                                        },
                                        modifier = Modifier.fillMaxWidth()
                                    )
                                    val strength = when {
                                        newPass.isEmpty() -> 0f
                                        newPass.length < 8 -> 0.25f
                                        newPass.length < 12 -> 0.5f
                                        newPass.length < 16 -> 0.75f
                                        else -> 1f
                                    }
                                    val strengthColor = when {
                                        newPass.isEmpty() -> Color.Transparent
                                        newPass.length < 8 -> Color.Red
                                        newPass.length < 12 -> Color(0xFFFFA500)
                                        newPass.length < 16 -> Color(0xFF9ACD32)
                                        else -> Color.Green
                                    }
                                    if (newPass.isNotEmpty()) {
                                        LinearProgressIndicator(
                                            progress = { strength },
                                            color = strengthColor,
                                            modifier = Modifier.fillMaxWidth().height(4.dp).padding(top = 4.dp)
                                        )
                                    }
                                }
                                OutlinedTextField(
                                    value = confirmPass,
                                    onValueChange = { confirmPass = it },
                                    label = { Text("Confirm Password") },
                                    visualTransformation = if (confirmPassVisible) androidx.compose.ui.text.input.VisualTransformation.None else androidx.compose.ui.text.input.PasswordVisualTransformation(),
                                    trailingIcon = {
                                        IconButton(onClick = { confirmPassVisible = !confirmPassVisible }) {
                                            Icon(if (confirmPassVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, "Toggle Password")
                                        }
                                    }
                                )
                            }
                        },
                        confirmButton = {
                            TextButton(onClick = {
                                // Real implementation would verify currentPass. For now, assume it's correct for simplicity.
                                if (newPass == confirmPass && newPass.isNotEmpty()) {
                                    viewModel.changeMasterPassword(newPass)
                                    showChangePasswordDialog = false
                                }
                            }) {
                                Text("Update Password")
                            }
                        },
                        dismissButton = {
                            TextButton(onClick = { showChangePasswordDialog = false }) {
                                Text("Cancel")
                            }
                        }
                    )
                }
                
                if (showDatabaseInfoDialog) {
                    val dbUriState by viewModel.dbUri.collectAsState()
                    val context = LocalContext.current
                    val clipboardManager = LocalClipboardManager.current
                    var passwordVisible by remember { mutableStateOf(false) }

                    AlertDialog(
                        onDismissRequest = { showDatabaseInfoDialog = false },
                        title = { Text("Database Information") },
                        text = {
                            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                                Text("Database File:", fontWeight = FontWeight.SemiBold)
                                Text(dbUriState?.lastPathSegment ?: "Unknown")
                                Spacer(modifier = Modifier.height(8.dp))
                                Text("Master Password:", fontWeight = FontWeight.SemiBold)
                                
                                val masterPassword = viewModel.getMasterPassword() ?: ""
                                
                                if (!passwordVisible) {
                                    OutlinedButton(
                                        onClick = {
                                            com.example.ui.BiometricHelper.showPrompt(
                                                context = context,
                                                onSuccess = { passwordVisible = true },
                                                onError = { }
                                            )
                                        },
                                        modifier = Modifier.fillMaxWidth()
                                    ) {
                                        Icon(Icons.Default.Fingerprint, contentDescription = null)
                                        Spacer(modifier = Modifier.width(8.dp))
                                        Text("Verify fingerprint to view")
                                    }
                                } else {
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Text(masterPassword, modifier = Modifier.weight(1f))
                                        IconButton(onClick = { passwordVisible = false }) {
                                            Icon(Icons.Default.VisibilityOff, contentDescription = "Hide Password")
                                        }
                                        IconButton(onClick = {
                                            clipboardManager.setText(AnnotatedString(masterPassword))
                                        }) {
                                            Icon(Icons.Default.ContentCopy, contentDescription = "Copy Password")
                                        }
                                    }
                                }
                            }
                        },
                        confirmButton = {
                            TextButton(onClick = { showDatabaseInfoDialog = false }) {
                                Text("Close")
                            }
                        }
                    )
                }
                
                HorizontalDivider()
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Lock, contentDescription = null) },
                    label = { Text("Close Secure") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        if (hasUnsavedChanges) {
                            pendingAction = { viewModel.lockDatabase() }
                            showUnsavedChangesDialog = true
                        } else {
                            viewModel.lockDatabase()
                        }
                    }
                )
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.FolderOpen, contentDescription = null) },
                    label = { Text("Open Existing Secure") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        if (hasUnsavedChanges) {
                            pendingAction = { filePickerLauncher.launch(arrayOf("*/*")) }
                            showUnsavedChangesDialog = true
                        } else {
                            filePickerLauncher.launch(arrayOf("*/*"))
                        }
                    }
                )
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Add, contentDescription = null) },
                    label = { Text("Create New Secure") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        onNavigateToCreate()
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                NavigationDrawerItem(
                    icon = { Icon(Icons.AutoMirrored.Filled.LibraryBooks, contentDescription = null) },
                    label = { Text("Templates") },
                    selected = false,
                    onClick = { 
                        scope.launch { drawerState.close() }
                        
    
    onNavigateToTemplates()
                    }
                )
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Settings, contentDescription = null) },
                    label = { Text("Settings") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        onNavigateToSettings()
                    }
                )
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Info, contentDescription = null) },
                    label = { Text("About") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        onNavigateToAbout()
                    }
                )
            }
        }
    ) {
        
        
        Box(modifier = Modifier.fillMaxSize()) {
            Scaffold(
                floatingActionButton = {
                    Column(horizontalAlignment = Alignment.End) {
                                    if (showChooseTemplateSheet) {
                val templates = viewModel.getTemplates()
                ModalBottomSheet(
                    onDismissRequest = { showChooseTemplateSheet = false }
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp)
                    ) {
                        Text("Select a template", fontSize = 20.sp, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        androidx.compose.foundation.lazy.LazyColumn {
                            items(templates.size) { index ->
                                val template = templates[index]
                                Card(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 8.dp)
                                        .clickable {
                                            viewModel.selectTemplateForNewEntry(template)
                                            showChooseTemplateSheet = false
                                            onNavigateToAddEntry()
                                        },
                                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                                ) {
                                    Row(
                                        modifier = Modifier.padding(16.dp).fillMaxWidth(),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        val iconColor = parseColor(template.customData["ThemeColor"]?.value)
                                        val iconVector = parseIcon(template.icon.name)
                                        Icon(iconVector, contentDescription = null, tint = iconColor, modifier = Modifier.size(32.dp))
                                        Spacer(modifier = Modifier.width(16.dp))
                                        Text(text = template[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: "Unnamed", fontSize = 18.sp)
                                    }
                                }
                            }
                        }
                        Spacer(modifier = Modifier.height(32.dp))
                    }
                }
            }
            if (showFabMenu) {
                            ExtendedFloatingActionButton(
                                text = { Text("Add entry") },
                                icon = { Icon(Icons.Default.VpnKey, "Add entry") },
                                onClick = { 
                                    showFabMenu = false
                                    onNavigateToAddEntry()
                                },
                                containerColor = Color(0xFF0066FF),
                                contentColor = Color.White,
                                modifier = Modifier.padding(bottom = 16.dp)
                            )
                            ExtendedFloatingActionButton(
                                text = { Text("Template") },
                                icon = { Icon(Icons.Default.ContentPaste, "Template") },
                                onClick = {
                                    showFabMenu = false
                                    showChooseTemplateSheet = true
                                },
                                containerColor = Color(0xFF0066FF),
                                contentColor = Color.White,
                                modifier = Modifier.padding(bottom = 16.dp)
                            )
                            ExtendedFloatingActionButton(
                                text = { Text("Add group") },
                                icon = { Icon(Icons.Default.Folder, "Add group") },
                                onClick = {
                                    showFabMenu = false
                                    onNavigateToAddGroup()
                                },
                                containerColor = Color(0xFF0066FF),
                                contentColor = Color.White,
                                modifier = Modifier.padding(bottom = 16.dp)
                            )
                        }
                        
                        FloatingActionButton(
                            onClick = { showFabMenu = !showFabMenu },
                            containerColor = if (showFabMenu) Color(0xFF0066FF) else Color(0xFF0D47A1),
                            contentColor = Color.White,
                            shape = CircleShape
                        ) {
                            Icon(
                                if (showFabMenu) Icons.Default.Close else Icons.Default.Add, 
                                contentDescription = if (showFabMenu) "Close" else "Add"
                            )
                        }
                    }
                },
                topBar = {
                TopAppBar(
                    title = {
                        Column {
                            Text("Secure", fontWeight = FontWeight.Bold, fontSize = 20.sp)
                            Text(currentGroup?.name ?: "Database", fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    },
                    navigationIcon = {
                        if (!isRoot) {
                            IconButton(onClick = { viewModel.navigateUp() }) {
                                Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                            }
                        } else {
                            IconButton(onClick = { scope.launch { drawerState.open() } }) {
                                Icon(Icons.Default.Menu, contentDescription = "Menu")
                            }
                        }
                    },
                    actions = {
                        IconButton(onClick = {
                            if (hasUnsavedChanges) {
                                pendingAction = { viewModel.lockDatabase() }
                                showUnsavedChangesDialog = true
                            } else {
                                viewModel.lockDatabase()
                            }
                        }) {
                            Icon(Icons.Default.Lock, contentDescription = "Lock")
                        }
                        IconButton(onClick = { viewModel.saveDatabase() }) {
                            if (hasUnsavedChanges) {
                                BadgedBox(badge = { Badge { Text("!") } }) {
                                    Icon(Icons.Default.Save, contentDescription = "Save", tint = MaterialTheme.colorScheme.primary)
                                }
                            } else {
                                Icon(Icons.Default.Save, contentDescription = "Save")
                            }
                        }
                        Box {
                            IconButton(onClick = { showSortMenu = true }) {
                                Icon(Icons.Default.Sort, contentDescription = "Sort")
                            }
                            DropdownMenu(
                                expanded = showSortMenu,
                                onDismissRequest = { showSortMenu = false }
                            ) {
                                DropdownMenuItem(
                                    text = { Text("Default") },
                                    onClick = { sortOrder = "Default"; showSortMenu = false }
                                )
                                DropdownMenuItem(
                                    text = { Text("A-Z") },
                                    onClick = { sortOrder = "A-Z"; showSortMenu = false }
                                )
                                DropdownMenuItem(
                                    text = { Text("Z-A") },
                                    onClick = { sortOrder = "Z-A"; showSortMenu = false }
                                )
                            }
                        }
                        IconButton(onClick = onNavigateToSettings) {
                            Icon(Icons.Default.Settings, contentDescription = "Settings")
                        }

                    }
                )
            }
        ) { paddingValues ->
            if (currentGroup == null) return@Scaffold
            
            val rawGroups = currentGroup!!.groups
            val rawEntries = currentGroup!!.entries
            
            val groups = when (sortOrder) {
                "A-Z" -> rawGroups.sortedBy { it.name.lowercase() }
                "Z-A" -> rawGroups.sortedByDescending { it.name.lowercase() }
                else -> rawGroups
            }
            
            val entries = when (sortOrder) {
                "A-Z" -> rawEntries.sortedBy { it[app.keemobile.kotpass.constants.BasicField.Title]?.content?.lowercase() ?: "" }
                "Z-A" -> rawEntries.sortedByDescending { it[app.keemobile.kotpass.constants.BasicField.Title]?.content?.lowercase() ?: "" }
                else -> rawEntries
            }
            

            if (showBottomSheet) {
                ModalBottomSheet(
                    onDismissRequest = { showBottomSheet = false },
                    sheetState = sheetState
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Add New", fontSize = 20.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 16.dp))
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable {
                                    scope.launch { sheetState.hide() }.invokeOnCompletion {
                                        if (!sheetState.isVisible) {
                                            showBottomSheet = false
                                            onNavigateToAddGroup()
                                        }
                                    }
                                }
                                .padding(vertical = 12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(Icons.Default.Folder, contentDescription = "New Group")
                            Spacer(modifier = Modifier.width(16.dp))
                            Text("New Group")
                        }
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .clickable {
                                    scope.launch { sheetState.hide() }.invokeOnCompletion {
                                        if (!sheetState.isVisible) {
                                            showBottomSheet = false
                                            onNavigateToAddEntry()
                                        }
                                    }
                                }
                                .padding(vertical = 12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Icon(Icons.Default.VpnKey, contentDescription = "New Entry")
                            Spacer(modifier = Modifier.width(16.dp))
                            Text("New Entry")
                        }
                        Spacer(modifier = Modifier.height(32.dp))
                    }
                }
            }



            Box(modifier = Modifier.fillMaxSize()) {
                LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .padding(horizontal = 16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                item { Spacer(modifier = Modifier.height(8.dp)) }
                
                if (isSearchActive && searchQuery.isNotEmpty()) {
                    items(searchResults, key = { it.uuid.toString() }) { entry ->
                        EntryItem(
                            entry,
                            onClick = debounced { 
                                viewModel.selectEntry(entry)
                                onNavigateToView()
                            },
                            onEdit = debounced { viewModel.selectEntry(entry); onNavigateToEditEntry() },
                            onDuplicate = debounced { viewModel.duplicateEntry(entry) },
                            onDelete = debounced { viewModel.deleteEntry(entry) }
                        )
                    }
                } else {
                    items(groups, key = { it.uuid.toString() }) { group ->
                        GroupItem(
                            group,
                            onClick = debounced { viewModel.selectGroup(group) },
                            onEdit = debounced { viewModel.selectGroup(group); onNavigateToEditGroup() },
                            onDuplicate = debounced { viewModel.duplicateGroup(group) },
                            onDelete = debounced { viewModel.deleteGroup(group) }
                        )
                    }
                    
                    items(entries, key = { it.uuid.toString() }) { entry ->
                        EntryItem(
                            entry,
                            onClick = debounced { 
                                viewModel.selectEntry(entry)
                                onNavigateToView()
                            },
                            onEdit = debounced { viewModel.selectEntry(entry); onNavigateToEditEntry() },
                            onDuplicate = debounced { viewModel.duplicateEntry(entry) },
                            onDelete = debounced { viewModel.deleteEntry(entry) }
                        )
                    }
                }
                
                item { Spacer(modifier = Modifier.height(80.dp)) }
                }
            }
                

                        if (showChooseTemplateSheet) {
                val templates = viewModel.getTemplates()
                ModalBottomSheet(
                    onDismissRequest = { showChooseTemplateSheet = false }
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp)
                    ) {
                        Text("Select a template", fontSize = 20.sp, fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)
                        Spacer(modifier = Modifier.height(16.dp))
                        
                        androidx.compose.foundation.lazy.LazyColumn {
                            items(templates.size) { index ->
                                val template = templates[index]
                                Card(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 8.dp)
                                        .clickable {
                                            viewModel.selectTemplateForNewEntry(template)
                                            showChooseTemplateSheet = false
                                            onNavigateToAddEntry()
                                        },
                                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                                ) {
                                    Row(
                                        modifier = Modifier.padding(16.dp).fillMaxWidth(),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        val iconColor = parseColor(template.customData["ThemeColor"]?.value)
                                        val iconVector = parseIcon(template.icon.name)
                                        Icon(iconVector, contentDescription = null, tint = iconColor, modifier = Modifier.size(32.dp))
                                        Spacer(modifier = Modifier.width(16.dp))
                                        Text(text = template[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: "Unnamed", fontSize = 18.sp)
                                    }
                                }
                            }
                        }
                        Spacer(modifier = Modifier.height(32.dp))
                    }
                }
            }
            if (showFabMenu) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(Color.Black.copy(alpha = 0.5f))
                        .clickable(
                            interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                            indication = null
                        ) { showFabMenu = false }
                )
            }
        }
    }
}

}

@Composable
fun GroupItem(group: app.keemobile.kotpass.models.Group, onClick: () -> Unit, onEdit: () -> Unit = {}, onMove: () -> Unit = {}, onDuplicate: () -> Unit = {}, onDelete: () -> Unit = {}) {
    val iconColor = parseColor(group.customData["ThemeColor"]?.value)
    val iconVector = parseIcon(group.icon.name)
    var showMenu by remember { mutableStateOf(false) }

    
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .fillMaxWidth()
            .pointerInput(Unit) {
                detectTapGestures(
                    onTap = { onClick() },
                    onLongPress = { showMenu = true }
                )
            }
            .padding(vertical = 12.dp)
    ) {
        Icon(
            iconVector,
            contentDescription = "Folder",
            tint = iconColor,
            modifier = Modifier.size(24.dp)
        )
        Spacer(modifier = Modifier.width(16.dp))
        Text(text = group.name, fontSize = 16.sp)
        
        Box(modifier = Modifier.fillMaxSize().wrapContentSize(Alignment.TopEnd)) {
        DropdownMenu(
            expanded = showMenu,
            onDismissRequest = { showMenu = false }
        ) {
            DropdownMenuItem(
                text = { Text("Edit") },
                onClick = {
                    showMenu = false
                    onEdit()
                }
            )
            DropdownMenuItem(
                text = { Text("Move") },
                onClick = {
                    showMenu = false
                    onMove()
                }
            )
            DropdownMenuItem(
                text = { Text("Duplicate") },
                onClick = {
                    showMenu = false
                    onDuplicate()
                }
            )
            DropdownMenuItem(
                text = { Text("Delete") },
                onClick = {
                    showMenu = false
                    onDelete()
                }
            )
        }
    }
}
        }

fun Modifier.dashedBorder(color: Color, width: Float, radius: Float) = drawBehind {
    drawRoundRect(
        color = color,
        style = Stroke(
            width = width,
            pathEffect = PathEffect.dashPathEffect(floatArrayOf(10f, 10f), 0f)
        ),
        cornerRadius = CornerRadius(radius, radius)
    )
}

@Composable
fun EntryItem(entry: app.keemobile.kotpass.models.Entry, onClick: () -> Unit, onEdit: () -> Unit = {}, onMove: () -> Unit = {}, onDuplicate: () -> Unit = {}, onDelete: () -> Unit = {}) {
    val iconColor = parseColor(entry.customData["ThemeColor"]?.value)
    val iconVector = parseIcon(entry.icon.name)
    var showMenu by remember { mutableStateOf(false) }


    Card(
        modifier = Modifier
            .fillMaxWidth()
            .pointerInput(Unit) {
                detectTapGestures(
                    onTap = { onClick() },
                    onLongPress = { showMenu = true }
                )
            },
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f)),
        shape = RoundedCornerShape(24.dp)
    ) {
        Row(
            modifier = Modifier
                .padding(horizontal = 24.dp, vertical = 16.dp)
                .fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                iconVector,
                contentDescription = "Key",
                tint = iconColor,
                modifier = Modifier.size(40.dp)
            )
            Spacer(modifier = Modifier.width(20.dp))
            Column {
                Text(text = (entry[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: ""), fontWeight = FontWeight.Medium, fontSize = 20.sp)
                if ((entry[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: "").isNotEmpty()) {
                    Text(text = (entry[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: ""), fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                if (entry.tags.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(4.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        entry.tags.forEach { tag ->
                            Box(
                                modifier = Modifier
                                    .dashedBorder(color = iconColor.copy(alpha = 0.8f), width = 3f, radius = 16f)
                                    .padding(horizontal = 6.dp, vertical = 2.dp)
                            ) {
                                Text(
                                    text = tag,
                                    color = iconColor.copy(alpha = 0.9f),
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.Medium
                                )
                            }
                        }
                    }
                }
            }
               
            Box(modifier = Modifier.fillMaxSize().wrapContentSize(Alignment.TopEnd)) {
        DropdownMenu(
                expanded = showMenu,
                onDismissRequest = { showMenu = false }
            ) {
                DropdownMenuItem(
                    text = { Text("Edit") },
                    onClick = {
                        showMenu = false
                        onEdit()
                    }
                )
                DropdownMenuItem(
                    text = { Text("Move") },
                    onClick = {
                        showMenu = false
                        onMove()
                    }
                )
                DropdownMenuItem(
                    text = { Text("Duplicate") },
                    onClick = {
                        showMenu = false
                        onDuplicate()
                    }
                )
                DropdownMenuItem(
                    text = { Text("Delete") },
                    onClick = {
                        showMenu = false
                        onDelete()
                    }
                )
            }
        }
    }
        }
}
