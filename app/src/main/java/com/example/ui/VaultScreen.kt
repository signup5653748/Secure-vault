package com.example.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.viewmodel.KeePassViewModel
import org.linguafranca.pwdb.Entry
import org.linguafranca.pwdb.Group

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun VaultScreen(
    viewModel: KeePassViewModel,
    onNavigateToView: () -> Unit
) {
    val currentGroup by viewModel.currentGroup.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text("Vault", fontWeight = FontWeight.Bold, fontSize = 20.sp)
                        Text(currentGroup?.name ?: "Database", fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                },
                navigationIcon = {
                    if (currentGroup?.parent != null) {
                        IconButton(onClick = { viewModel.navigateUp() }) {
                            Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                        }
                    } else {
                        IconButton(onClick = { /* Menu */ }) {
                            Icon(Icons.Default.Menu, contentDescription = "Menu")
                        }
                    }
                },
                actions = {
                    IconButton(onClick = { viewModel.lockDatabase() }) {
                        Icon(Icons.Default.Lock, contentDescription = "Lock")
                    }
                }
            )
        }
    ) { paddingValues ->
        if (currentGroup == null) return@Scaffold
        
        val groups = currentGroup!!.groups
        val entries = currentGroup!!.entries

        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            item { Spacer(modifier = Modifier.height(8.dp)) }
            
            items(groups) { group ->
                GroupItem(group, onClick = { viewModel.selectGroup(group) })
            }
            
            items(entries) { entry ->
                EntryItem(entry, onClick = { 
                    viewModel.selectEntry(entry)
                    onNavigateToView()
                })
            }
            
            item { Spacer(modifier = Modifier.height(16.dp)) }
        }
    }
}

@Composable
fun GroupItem(group: Group<*, *, *, *>, onClick: () -> Unit) {
    Row(
        verticalAlignment = Alignment.CenterVertically,
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(vertical = 12.dp)
    ) {
        Icon(
            Icons.Default.Folder,
            contentDescription = "Folder",
            tint = MaterialTheme.colorScheme.onSurface,
            modifier = Modifier.size(24.dp)
        )
        Spacer(modifier = Modifier.width(16.dp))
        Text(text = group.name, fontSize = 16.sp)
    }
}

@Composable
fun EntryItem(entry: Entry<*, *, *, *>, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f))
    ) {
        Row(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                Icons.Default.VpnKey,
                contentDescription = "Key",
                tint = MaterialTheme.colorScheme.primary,
                modifier = Modifier.size(32.dp)
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(text = entry.title, fontWeight = FontWeight.Medium, fontSize = 18.sp)
                if (entry.username.isNotEmpty()) {
                    Text(text = entry.username, fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
    }
}
