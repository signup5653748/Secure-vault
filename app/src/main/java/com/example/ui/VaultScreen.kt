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
import androidx.compose.material.icons.automirrored.filled.ArrowBack
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
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.background
import androidx.compose.ui.graphics.Color
import com.example.viewmodel.KeePassViewModel
import app.keemobile.kotpass.models.Group
import app.keemobile.kotpass.models.Entry
import kotlinx.coroutines.launch
import app.keemobile.kotpass.constants.BasicField
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun VaultScreen(
    viewModel: KeePassViewModel,
    onNavigateToView: () -> Unit,
    onNavigateToSettings: () -> Unit = {},
    onNavigateToCreate: () -> Unit = {},
    onNavigateToAbout: () -> Unit = {},
    onNavigateToAddEntry: () -> Unit = {},
    onNavigateToTemplates: () -> Unit = {},
    onNavigateToAddTemplate: () -> Unit = {},
    onNavigateToAddGroup: () -> Unit = {},
    onNavigateToAddNote: () -> Unit = {}
) {
    val database by viewModel.database.collectAsState()
    val currentGroup by viewModel.currentGroup.collectAsState()
    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
    BackHandler(enabled = !viewModel.isRootGroup()) {

        viewModel.navigateUp()

    }
    val scope = rememberCoroutineScope()
    
    LaunchedEffect(Unit) {
        viewModel.getOrCreateTemplatesGroup()
    }
    
    var showBottomSheet by remember { mutableStateOf(false) }


    var showFabMenu by remember { mutableStateOf(false) }
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
                Text(
                    "Vault",
                    modifier = Modifier.padding(16.dp),
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.primary
                )
                HorizontalDivider()
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Lock, contentDescription = null) },
                    label = { Text("Close Vault") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        viewModel.lockDatabase()
                    }
                )
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.FolderOpen, contentDescription = null) },
                    label = { Text("Open Existing Vault") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        filePickerLauncher.launch(arrayOf("*/*"))
                    }
                )
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Add, contentDescription = null) },
                    label = { Text("Create New Vault") },
                    selected = false,
                    onClick = {
                        scope.launch { drawerState.close() }
                        onNavigateToCreate()
                    }
                )
                HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.LibraryBooks, contentDescription = null) },
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
                            Text("Vault", fontWeight = FontWeight.Bold, fontSize = 20.sp)
                            Text(currentGroup?.name ?: "Database", fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    },
                    navigationIcon = {
                        if (!viewModel.isRootGroup()) {
                            IconButton(onClick = { viewModel.navigateUp() }) {
                                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                            }
                        } else {
                            IconButton(onClick = { scope.launch { drawerState.open() } }) {
                                Icon(Icons.Default.Menu, contentDescription = "Menu")
                            }
                        }
                    },
                    actions = {
                        IconButton(onClick = onNavigateToSettings) {
                            Icon(Icons.Default.Settings, contentDescription = "Settings")
                        }

                    }
                )
            }
        ) { paddingValues ->
            if (currentGroup == null) return@Scaffold
            
            val groups = currentGroup!!.groups
            val entries = currentGroup!!.entries
            

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
                            onClick = { 
                                viewModel.selectEntry(entry)
                                onNavigateToView()
                            },
                            onDelete = { viewModel.deleteEntry(entry) }
                        )
                    }
                } else {
                    items(groups, key = { it.uuid.toString() }) { group ->
                        GroupItem(
                            group,
                            onClick = { viewModel.selectGroup(group) },
                            onDelete = { viewModel.deleteGroup(group) }
                        )
                    }
                    
                    items(entries, key = { it.uuid.toString() }) { entry ->
                        EntryItem(
                            entry,
                            onClick = { 
                                viewModel.selectEntry(entry)
                                onNavigateToView()
                            },
                            onDelete = { viewModel.deleteEntry(entry) }
                        )
                    }
                }
                
                item { Spacer(modifier = Modifier.height(80.dp)) }
                }
                
                FloatingActionButton(
                    onClick = { viewModel.lockDatabase() },
                    containerColor = Color(0xFF0D47A1),
                    contentColor = Color.White,
                    shape = androidx.compose.foundation.shape.RoundedCornerShape(16.dp),
                    modifier = Modifier
                        .align(Alignment.BottomStart)
                        .padding(start = 16.dp, bottom = 16.dp)
                ) {
                    Icon(Icons.Default.Lock, contentDescription = "Lock")
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
fun GroupItem(group: app.keemobile.kotpass.models.Group, onClick: () -> Unit, onEdit: () -> Unit = {}, onMove: () -> Unit = {}, onDelete: () -> Unit = {}) {
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

@Composable
fun EntryItem(entry: app.keemobile.kotpass.models.Entry, onClick: () -> Unit, onEdit: () -> Unit = {}, onMove: () -> Unit = {}, onDelete: () -> Unit = {}) {
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
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
    ) {
        Row(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                iconVector,
                contentDescription = "Key",
                tint = iconColor,
                modifier = Modifier.size(32.dp)
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(text = (entry[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: ""), fontWeight = FontWeight.Medium, fontSize = 18.sp)
                if ((entry[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: "").isNotEmpty()) {
                    Text(text = (entry[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: ""), fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
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
