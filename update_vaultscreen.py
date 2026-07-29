import re

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "r") as f:
    content = f.read()

# Fix imports
imports = """import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.rememberModalBottomSheetState
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.foundation.shape.CircleShape
"""
content = content.replace("import androidx.compose.runtime.rememberCoroutineScope", imports + "import androidx.compose.runtime.rememberCoroutineScope")

# Update signature
old_sig = """fun VaultScreen(
    viewModel: KeePassViewModel,
    onNavigateToView: () -> Unit,
    onNavigateToSettings: () -> Unit = {},
    onNavigateToCreate: () -> Unit = {},
    onNavigateToAbout: () -> Unit = {}
)"""

new_sig = """fun VaultScreen(
    viewModel: KeePassViewModel,
    onNavigateToView: () -> Unit,
    onNavigateToSettings: () -> Unit = {},
    onNavigateToCreate: () -> Unit = {},
    onNavigateToAbout: () -> Unit = {},
    onNavigateToAddEntry: () -> Unit = {}
)"""
content = content.replace(old_sig, new_sig)

# Add state for bottom sheet
state_code = """    val scope = rememberCoroutineScope()
    
    var showBottomSheet by remember { mutableStateOf(false) }
    var showNewGroupDialog by remember { mutableStateOf(false) }
    val sheetState = rememberModalBottomSheetState()"""
content = content.replace("    val scope = rememberCoroutineScope()", state_code)

# Add Scaffold FAB
fab_code = """        Scaffold(
            floatingActionButton = {
                FloatingActionButton(onClick = { showBottomSheet = true }, shape = CircleShape) {
                    Icon(Icons.Default.Add, contentDescription = "Add")
                }
            },
            topBar = {"""
content = content.replace("        Scaffold(\n            topBar = {", fab_code)

# Add Bottom sheet and Dialogs before the end of the Scaffold block
# Wait, let's insert it inside the Scaffold body or just before `LazyColumn`. Actually, they are overlays, they should be at the root or within Scaffold but not necessarily inside LazyColumn.

overlay_code = """
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
                                            showNewGroupDialog = true
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

            if (showNewGroupDialog) {
                var groupName by remember { mutableStateOf("") }
                var groupIcon by remember { mutableStateOf("Folder") }
                var groupColor by remember { mutableStateOf("Blue") }
                AlertDialog(
                    onDismissRequest = { showNewGroupDialog = false },
                    title = { Text("New Group") },
                    text = {
                        Column {
                            OutlinedTextField(
                                value = groupName,
                                onValueChange = { groupName = it },
                                label = { Text("Group Name") }
                            )
                            // Placeholder for Icon & Color picker
                            Text("Icon: $groupIcon", modifier = Modifier.padding(top = 8.dp))
                            Text("Color: $groupColor")
                        }
                    },
                    confirmButton = {
                        TextButton(onClick = {
                            viewModel.createGroup(groupName, groupIcon, groupColor)
                            showNewGroupDialog = false
                        }) {
                            Text("Create")
                        }
                    },
                    dismissButton = {
                        TextButton(onClick = { showNewGroupDialog = false }) {
                            Text("Cancel")
                        }
                    }
                )
            }
"""

content = content.replace("            LazyColumn(", overlay_code + "            LazyColumn(")

with open("app/src/main/java/com/example/ui/VaultScreen.kt", "w") as f:
    f.write(content)
