import re

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'r') as f:
    content = f.read()

new_imports = """import androidx.compose.ui.text.input.ImeAction
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material3.OutlinedTextField
"""

content = content.replace("import androidx.compose.material.icons.filled.Info", "import androidx.compose.material.icons.filled.Info\n" + new_imports)

search_state = """    var showFabMenu by remember { mutableStateOf(false) }
    val sheetState = rememberModalBottomSheetState()
    
    val searchQuery by viewModel.searchQuery.collectAsState()
    val searchResults by viewModel.searchResults.collectAsState()
    var isSearchActive by remember { mutableStateOf(false) }
"""

content = content.replace("""    var showFabMenu by remember { mutableStateOf(false) }
    val sheetState = rememberModalBottomSheetState()""", search_state)


top_app_bar_old = """                topBar = {
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
            }"""

top_app_bar_new = """                topBar = {
                if (isSearchActive) {
                    TopAppBar(
                        title = {
                            OutlinedTextField(
                                value = searchQuery,
                                onValueChange = { viewModel.setSearchQuery(it) },
                                placeholder = { Text("Search vault...") },
                                singleLine = true,
                                modifier = Modifier.fillMaxWidth().padding(end = 8.dp),
                                trailingIcon = {
                                    IconButton(onClick = { 
                                        viewModel.setSearchQuery("")
                                        isSearchActive = false
                                    }) {
                                        Icon(Icons.Default.Clear, contentDescription = "Clear")
                                    }
                                }
                            )
                        }
                    )
                } else {
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
                            IconButton(onClick = { isSearchActive = true }) {
                                Icon(Icons.Default.Search, contentDescription = "Search")
                            }
                            IconButton(onClick = onNavigateToSettings) {
                                Icon(Icons.Default.Settings, contentDescription = "Settings")
                            }
                        }
                    )
                }
            }"""

content = content.replace(top_app_bar_old, top_app_bar_new)

list_old = """            Box(modifier = Modifier.fillMaxSize()) {
                LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .padding(horizontal = 16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                item { Spacer(modifier = Modifier.height(8.dp)) }
                
                items(groups) { group ->
                    GroupItem(
                        group,
                        onClick = { viewModel.selectGroup(group) },
                        onDelete = { viewModel.deleteGroup(group) }
                    )
                }
                
                items(entries) { entry ->
                    EntryItem(
                        entry,
                        onClick = { 
                            viewModel.selectEntry(entry)
                            onNavigateToView()
                        },
                        onDelete = { viewModel.deleteEntry(entry) }
                    )
                }
                
                item { Spacer(modifier = Modifier.height(80.dp)) }
                }"""

list_new = """            Box(modifier = Modifier.fillMaxSize()) {
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
                }"""

content = content.replace(list_old, list_new)

with open('/app/applet/app/src/main/java/com/example/ui/VaultScreen.kt', 'w') as f:
    f.write(content)

