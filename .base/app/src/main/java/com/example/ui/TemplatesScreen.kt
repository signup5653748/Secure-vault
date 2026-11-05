package com.example.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.viewmodel.KeePassViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TemplatesScreen(viewModel: KeePassViewModel, onNavigateBack: () -> Unit, onNavigateToAddTemplate: () -> Unit, onNavigateToEditTemplate: () -> Unit = {}) {
    val database by viewModel.database.collectAsState()
    val currentTemplates = viewModel.getTemplates()

    LaunchedEffect(Unit) {
        viewModel.getOrCreateTemplatesGroup()
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Templates") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        },
        floatingActionButton = {
            var isNavigating by remember { mutableStateOf(false) }
            FloatingActionButton(
                onClick = {
                    if (!isNavigating) {
                        isNavigating = true
                        onNavigateToAddTemplate()
                    }
                },
                containerColor = Color(0xFF0066FF),
                contentColor = Color.White
            ) {
                Icon(Icons.Default.Add, contentDescription = "Add Template")
            }
        }
    ) { paddingValues ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            item { Spacer(modifier = Modifier.height(8.dp)) }
            items(currentTemplates, key = { it.uuid.toString() }) { template ->
                var showMenu by remember { mutableStateOf(false) }
                Card(
                    modifier = Modifier.fillMaxWidth().clickable { 
                        viewModel.selectEntry(template)
                        onNavigateToEditTemplate()
                    },
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        val iconVector = parseIcon(template.icon.name)
                        val iconColor = parseColor(template.customData["ThemeColor"]?.value)
                        Icon(iconVector, contentDescription = null, tint = iconColor, modifier = Modifier.size(32.dp))
                        Spacer(modifier = Modifier.width(16.dp))
                        Text(
                            text = template[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: "Unnamed",
                            fontSize = 18.sp,
                            modifier = Modifier.weight(1f)
                        )
                        Box {
                            IconButton(onClick = { showMenu = true }) {
                                Icon(Icons.Default.MoreVert, contentDescription = "More")
                            }
                            DropdownMenu(expanded = showMenu, onDismissRequest = { showMenu = false }) {
                                DropdownMenuItem(
                                    text = { Text("Edit / Rename") },
                                    onClick = { 
                                        showMenu = false
                                        viewModel.selectEntry(template)
                                        onNavigateToEditTemplate()
                                    }
                                )
                                DropdownMenuItem(
                                    text = { Text("Duplicate") },
                                    onClick = {
                                        showMenu = false
                                        val title = (template[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: "Unnamed") + " (Copy)"
                                        val username = template[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: ""
                                        val password = template[app.keemobile.kotpass.constants.BasicField.Password]?.content ?: ""
                                        val url = template[app.keemobile.kotpass.constants.BasicField.Url]?.content ?: ""
                                        val notes = template[app.keemobile.kotpass.constants.BasicField.Notes]?.content ?: ""
                                        
                                        val customFieldsData = mutableListOf<com.example.ui.CustomFieldData>()
                                        for ((key, value) in template.fields) {
                                            if (!key.contains("___")) continue
                                            val name = key.substringAfter("___")
                                            customFieldsData.add(com.example.ui.CustomFieldData(
                                                name = name,
                                                value = value.content,
                                                isHidden = value is app.keemobile.kotpass.models.EntryValue.Encrypted,
                                                showCopyButton = true
                                            ))
                                        }
                                        val hiddenFields = mutableListOf<String>()
                                        if (template.customData["Hide_UserName"]?.value == "true") hiddenFields.add("Hide_UserName")
                                        if (template.customData["Hide_Password"]?.value == "true") hiddenFields.add("Hide_Password")
                                        if (template.customData["Hide_Url"]?.value == "true") hiddenFields.add("Hide_Url")
                                        if (template.customData["Hide_Notes"]?.value == "true") hiddenFields.add("Hide_Notes")
                                        
                                        viewModel.addTemplate(title, username, password, url, notes, template.icon.name, template.customData["ThemeColor"]?.value ?: "Blue", customFieldsData, hiddenFields)
                                    }
                                )
                                DropdownMenuItem(
                                    text = { Text("Delete", color = Color.Red) },
                                    onClick = { 
                                        showMenu = false
                                        viewModel.deleteTemplate(template) 
                                    }
                                )
                            }
                        }
                    }
                }
            }
            item { Spacer(modifier = Modifier.height(80.dp)) }
        }
    }
}
