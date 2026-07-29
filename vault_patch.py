with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

# Add to signature
sig_old = """fun VaultScreen(
    viewModel: KeePassViewModel,
    onNavigateToView: () -> Unit,
    onNavigateToSettings: () -> Unit,
    onNavigateToCreate: () -> Unit,
    onNavigateToAbout: () -> Unit,
    onNavigateToAddEntry: () -> Unit
) {"""

sig_new = """fun VaultScreen(
    viewModel: KeePassViewModel,
    onNavigateToView: () -> Unit,
    onNavigateToSettings: () -> Unit,
    onNavigateToCreate: () -> Unit,
    onNavigateToAbout: () -> Unit,
    onNavigateToAddEntry: () -> Unit,
    onNavigateToTemplates: () -> Unit,
    onNavigateToAddNote: () -> Unit
) {"""
content = content.replace(sig_old, sig_new)

# Add Template sheet states
import_old = "var showNewGroupDialog by remember { mutableStateOf(false) }"
import_new = """var showNewGroupDialog by remember { mutableStateOf(false) }
    var showTemplateSheet by remember { mutableStateOf(false) }
    val templateSheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)"""
content = content.replace(import_old, import_new)

# Add "Template" to FAB menu
fab_menu_old = """                            ExtendedFloatingActionButton(
                                text = { Text("Add entry") },
                                icon = { Icon(Icons.Default.VpnKey, "Add entry") },
                                onClick = { 
                                    showFabMenu = false
                                    onNavigateToAddEntry()
                                },
                                containerColor = Color(0xFF0066FF),
                                contentColor = Color.White,
                                modifier = Modifier.padding(bottom = 16.dp)
                            )"""
fab_menu_new = """                            ExtendedFloatingActionButton(
                                text = { Text("Template") },
                                icon = { Icon(Icons.Default.LibraryAdd, "Template") },
                                onClick = { 
                                    showFabMenu = false
                                    showTemplateSheet = true
                                },
                                containerColor = Color(0xFF0066FF),
                                contentColor = Color.White,
                                modifier = Modifier.padding(bottom = 16.dp)
                            )
""" + fab_menu_old
content = content.replace(fab_menu_old, fab_menu_new)

# Add "Templates" to NavigationDrawerItem
drawer_item_old = """                NavigationDrawerItem(
                    icon = { Icon(Icons.Default.Settings, contentDescription = null) },
                    label = { Text("Settings") },"""
drawer_item_new = """                NavigationDrawerItem(
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
                    label = { Text("Settings") },"""
content = content.replace(drawer_item_old, drawer_item_new)

# Add Template bottom sheet
template_sheet_code = """
            if (showTemplateSheet) {
                val templates = viewModel.getTemplates()
                ModalBottomSheet(
                    onDismissRequest = { showTemplateSheet = false },
                    sheetState = templateSheetState
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text("Select Template", fontSize = 20.sp, fontWeight = FontWeight.Bold, modifier = Modifier.padding(bottom = 16.dp))
                        
                        LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                            items(templates) { template ->
                                Card(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clickable {
                                            scope.launch { templateSheetState.hide() }.invokeOnCompletion {
                                                if (!templateSheetState.isVisible) {
                                                    showTemplateSheet = false
                                                    val type = template.customData["TemplateType"]?.value
                                                    if (type == "Note") {
                                                        onNavigateToAddNote()
                                                    } else {
                                                        viewModel.createEntryFromTemplate(template)
                                                    }
                                                }
                                            }
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
                                        Text(text = template[BasicField.Title]?.content ?: "Unnamed", fontSize = 18.sp)
                                    }
                                }
                            }
                        }
                        Spacer(modifier = Modifier.height(32.dp))
                    }
                }
            }
"""

content = content.replace("            if (showNewGroupDialog) {", template_sheet_code + "            if (showNewGroupDialog) {")

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
    f.write(content)
