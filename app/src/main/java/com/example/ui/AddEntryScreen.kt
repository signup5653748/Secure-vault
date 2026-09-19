package com.example.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.*
import androidx.compose.material.icons.automirrored.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.foundation.border

import androidx.compose.foundation.clickable

import androidx.compose.ui.draw.clip

import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.background
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.platform.ClipboardManager
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.foundation.gestures.detectDragGesturesAfterLongPress
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.material.icons.filled.DragHandle
import androidx.compose.foundation.gestures.detectDragGestures

import androidx.compose.foundation.gestures.detectTapGestures

import kotlin.math.min

import kotlin.math.sqrt

import kotlin.math.atan2

import kotlin.math.cos

import kotlin.math.sin

import androidx.compose.ui.input.pointer.pointerInput

import androidx.compose.ui.graphics.toArgb

import androidx.compose.foundation.shape.CircleShape

import androidx.compose.foundation.lazy.grid.GridCells

import androidx.compose.foundation.lazy.grid.LazyVerticalGrid

import androidx.compose.foundation.lazy.grid.items
import androidx.compose.material3.TextButton
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.rememberModalBottomSheetState
import kotlinx.coroutines.launch

import com.example.viewmodel.KeePassViewModel

data class CustomFieldData(val id: String = java.util.UUID.randomUUID().toString(), val name: String, val value: String, val isHidden: Boolean, val showCopyButton: Boolean)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddEntryScreen(
    viewModel: KeePassViewModel,
    onNavigateBack: () -> Unit,
    isTemplate: Boolean = false,
    isEdit: Boolean = false
) {
    val currentEntry by viewModel.currentEntry.collectAsState()
        val selectedTemplate by viewModel.selectedTemplate.collectAsState()
    
    
    var title by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!![app.keemobile.kotpass.constants.BasicField.Title]?.content ?: "" else "") }
    var username by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!![app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: "" else "") }
    var password by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!![app.keemobile.kotpass.constants.BasicField.Password]?.content ?: "" else "") }
    var url by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!![app.keemobile.kotpass.constants.BasicField.Url]?.content ?: "" else "") }
    var notes by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!![app.keemobile.kotpass.constants.BasicField.Notes]?.content ?: "" else "") }
    var iconName by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.icon.name else "Key") }
    var color by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.customData["ThemeColor"]?.value ?: "Blue" else "Blue") }
    var tagsString by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.tags.joinToString(", ") else "") }
    var fieldOrder by remember(currentEntry?.uuid) { mutableStateOf(listOf("Username", "Password", "URL", "Notes")) }

    var showUsername by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.fields.containsKey(app.keemobile.kotpass.constants.BasicField.UserName()) && currentEntry!!.customData["Hide_UserName"]?.value != "true" else !isTemplate) }
    var showPassword by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.fields.containsKey(app.keemobile.kotpass.constants.BasicField.Password()) && currentEntry!!.customData["Hide_Password"]?.value != "true" else !isTemplate) }
    var showUrl by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.fields.containsKey(app.keemobile.kotpass.constants.BasicField.Url()) && currentEntry!!.customData["Hide_Url"]?.value != "true" else !isTemplate) }
    var showNotes by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) currentEntry!!.fields.containsKey(app.keemobile.kotpass.constants.BasicField.Notes()) && currentEntry!!.customData["Hide_Notes"]?.value != "true" else !isTemplate) }
    
    var customFields by remember(currentEntry?.uuid) { mutableStateOf(if (isEdit && currentEntry != null) {
        val newCustomFields = mutableListOf<CustomFieldData>()
        val basicFields = listOf(app.keemobile.kotpass.constants.BasicField.Title(), app.keemobile.kotpass.constants.BasicField.UserName(), app.keemobile.kotpass.constants.BasicField.Password(), app.keemobile.kotpass.constants.BasicField.Url(), app.keemobile.kotpass.constants.BasicField.Notes())
        for ((key, value) in currentEntry!!.fields) {
            if (key !in basicFields && key != "Notes" && key != "Title" && key != "UserName" && key != "URL" && key != "Password") {
                val fieldName = key
                val isHidden = value is app.keemobile.kotpass.models.EntryValue.Encrypted
                val fieldValue = value.content
                val showCopy = currentEntry!!.customData["ShowCopyButton_$fieldName"]?.value == "true"
                newCustomFields.add(CustomFieldData(
                    name = fieldName,
                    value = fieldValue,
                    isHidden = isHidden,
                    showCopyButton = showCopy
                ))
            }
        }
        newCustomFields.toList()
    } else {
        listOf<CustomFieldData>()
    }) }

    LaunchedEffect(selectedTemplate) {
        if (selectedTemplate != null && !isEdit) {
            val template = selectedTemplate!!
            title = template[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: ""
            username = template[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: ""
            password = template[app.keemobile.kotpass.constants.BasicField.Password]?.content ?: ""
            url = template[app.keemobile.kotpass.constants.BasicField.Url]?.content ?: ""
            notes = template[app.keemobile.kotpass.constants.BasicField.Notes]?.content ?: ""
            iconName = template.icon.name
            color = template.customData["ThemeColor"]?.value ?: "Blue"
            tagsString = template.tags.joinToString(", ")
            
            showUsername = template.customData["Hide_UserName"]?.value != "true"
            showPassword = template.customData["Hide_Password"]?.value != "true"
            showUrl = template.customData["Hide_Url"]?.value != "true"
            showNotes = template.customData["Hide_Notes"]?.value != "true"
            
            val newCustomFields = mutableListOf<CustomFieldData>()
            val basicFields = listOf(app.keemobile.kotpass.constants.BasicField.Title(), app.keemobile.kotpass.constants.BasicField.UserName(), app.keemobile.kotpass.constants.BasicField.Password(), app.keemobile.kotpass.constants.BasicField.Url(), app.keemobile.kotpass.constants.BasicField.Notes())
            
            for ((key, value) in template.fields) {
                if (key !in basicFields) {
                    val fieldName = key
                    val isHidden = value is app.keemobile.kotpass.models.EntryValue.Encrypted
                    val fieldValue = value.content
                    val showCopy = template.customData["ShowCopyButton_$fieldName"]?.value == "true"
                    newCustomFields.add(CustomFieldData(name = fieldName, value = fieldValue, isHidden = isHidden, showCopyButton = showCopy))
                }
            }
            customFields = newCustomFields
            viewModel.selectTemplateForNewEntry(null)
        }
    }
    var isDeleteMode by remember { mutableStateOf(false) }
    var isReorderMode by remember { mutableStateOf(false) }
    var selectedFieldsToDelete by remember { mutableStateOf(setOf<String>()) }
    var showPasswordGenerator by remember { mutableStateOf(false) }
    var showAddFieldDialog by remember { mutableStateOf(false) }
    var showIconDialog by remember { mutableStateOf(false) }
    var showColorDialog by remember { mutableStateOf(false) }
    var showAttachmentsDialog by remember { mutableStateOf(false) }
    var attachments by remember { mutableStateOf(listOf<String>()) }
    var showMoreMenu by remember { mutableStateOf(false) }
    val predefinedIcons = listOf(
        "Key", "Lock", "Person", "CreditCard", 
        "Folder", "Mail", "Phone", "Build", 
        "Settings", "Favorite", "Star", "Home"
    )
    var isSaving by remember { mutableStateOf(false) }

    val clipboardManager: ClipboardManager = LocalClipboardManager.current

    var showTemplateSheet by remember { mutableStateOf(false) }
    val templateSheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
    val templates = remember(viewModel, showTemplateSheet) { viewModel.getTemplates() }
    val scope = rememberCoroutineScope()


    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(if (isEdit) "Edit Entry" else if (isTemplate) "New Template" else "New Entry") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    if (isDeleteMode) {
                        TextButton(onClick = { 
                            isDeleteMode = false
                            selectedFieldsToDelete = setOf()
                        }) {
                            Text("Cancel")
                        }
                    } else {

                        Box {
                            IconButton(onClick = { showMoreMenu = true }) {
                                Icon(Icons.Default.MoreVert, contentDescription = "More options")
                            }
                            DropdownMenu(
                                expanded = showMoreMenu,
                                onDismissRequest = { showMoreMenu = false }
                            ) {
                                DropdownMenuItem(
                                    text = { Text("Delete Fields") },
                                    onClick = {
                                        showMoreMenu = false
                                        isDeleteMode = true
                                        isReorderMode = false
                                        selectedFieldsToDelete = setOf()
                                    }
                                )
                                DropdownMenuItem(
                                    text = { Text("Reorder Fields") },
                                    onClick = {
                                        showMoreMenu = false
                                        isReorderMode = true
                                        isDeleteMode = false
                                    }
                                )
                            }
                        }
                    }
                }

            )
        },
        bottomBar = {
            if (isDeleteMode) {
                BottomAppBar(containerColor = MaterialTheme.colorScheme.surfaceVariant) {
                    Spacer(modifier = Modifier.weight(1f))
                    Button(
                        onClick = {
                            if (selectedFieldsToDelete.contains("Username")) { showUsername = false; username = "" }
                            if (selectedFieldsToDelete.contains("Password")) { showPassword = false; password = "" }
                            if (selectedFieldsToDelete.contains("URL")) { showUrl = false; url = "" }
                            if (selectedFieldsToDelete.contains("Notes")) { showNotes = false; notes = "" }
                            
                            val customFieldsToDelete = selectedFieldsToDelete.filter { it.startsWith("Custom:") }.map { it.substringAfter("Custom:") }
                            if (customFieldsToDelete.isNotEmpty()) {
                                customFields = customFields.filter { it.name !in customFieldsToDelete }
                            }
                            
                            isDeleteMode = false
                            selectedFieldsToDelete = setOf()
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color.Red)
                    ) {
                        Text("Delete / Done")
                    }
                    Spacer(modifier = Modifier.weight(1f))
                }
            } else if (isReorderMode) {
                BottomAppBar(containerColor = MaterialTheme.colorScheme.surfaceVariant) {
                    Spacer(modifier = Modifier.weight(1f))
                    Button(onClick = { isReorderMode = false }) {
                        Text("Done Reordering")
                    }
                    Spacer(modifier = Modifier.weight(1f))
                }
            } else {
                BottomAppBar {
                    if (!isTemplate) {
                        IconButton(onClick = { /* Lock */ }) {
                            Icon(Icons.Default.Lock, contentDescription = "Lock Entry")
                        }
                        IconButton(onClick = { showAttachmentsDialog = true }) {
                            Icon(Icons.Default.AttachFile, contentDescription = "Attachments")
                        }
                    }
                    IconButton(onClick = { showAddFieldDialog = true }) {
                        Icon(Icons.Default.Add, contentDescription = "Add Field")
                    }
    
                    Spacer(modifier = Modifier.weight(1f))
                    IconButton(onClick = {
                        if (!isSaving) {
                            isSaving = true
                                                        val u = if (showUsername) username else null
                            val p = if (showPassword) password else null
                            val ur = if (showUrl) url else null
                            val n = if (showNotes) notes else null
                            val tagsList = tagsString.split(",").map { it.trim() }.filter { it.isNotEmpty() }
                            
                            if (isEdit && isTemplate) {
                                viewModel.updateEntry(title, u, p, ur, n, iconName, color, customFields, tagsList)
                            } else if (isEdit) {
                                viewModel.updateEntry(title, u, p, ur, n, iconName, color, customFields, tagsList)
                            } else if (isTemplate) {
                                viewModel.addTemplate(title, u, p, ur, n, iconName, color, customFields, tagsList)
                            } else {
                                viewModel.createEntry(title, u, p, ur, n, iconName, color, customFields, tagsList)
                            }
                            onNavigateBack()
                        }
                    }) {
                        Icon(Icons.Default.Check, contentDescription = "Save")
                    }
                }
            }
        }
    ) { paddingValues ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            item { Spacer(modifier = Modifier.height(8.dp)) }
            

            item {

                Row(

                    modifier = Modifier.fillMaxWidth(),

                    horizontalArrangement = Arrangement.Center,

                    verticalAlignment = Alignment.CenterVertically

                ) {

                    Spacer(modifier = Modifier.width(48.dp))

                    Box(

                        modifier = Modifier

                            .size(80.dp)

                            .background(Color.Transparent, CircleShape)

                            .border(2.dp, parseColor(color), CircleShape)

                            .clickable { showIconDialog = true },

                        contentAlignment = Alignment.Center

                    ) {

                        val iconColor = parseColor(color)

                        val iconVector = parseIcon(iconName)

                        Icon(iconVector, contentDescription = "Select Icon", tint = iconColor, modifier = Modifier.size(40.dp))

                    }

                    Spacer(modifier = Modifier.width(16.dp))

                    IconButton(onClick = { showColorDialog = true }) {

                        Icon(Icons.Default.Palette, contentDescription = "Select Color", tint = parseColor(color))

                    }

                }

            }
            item {
                OutlinedTextField(
                    value = title,
                    onValueChange = { title = it },
                    label = { Text("Title") },
                    modifier = Modifier.fillMaxWidth()
                )
            }
            items(fieldOrder.size) { index ->
                val field = fieldOrder[index]
                
                if (field == "Username" && showUsername) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        if (isDeleteMode) {
                            Checkbox(checked = selectedFieldsToDelete.contains("Username"), onCheckedChange = { checked ->
                                if (checked) selectedFieldsToDelete = selectedFieldsToDelete + "Username" else selectedFieldsToDelete = selectedFieldsToDelete - "Username"
                            })
                        }
                        if (isReorderMode) {
                            Icon(
                                Icons.Default.DragHandle, 
                                contentDescription = "Reorder",
                                modifier = Modifier
                                    .padding(end = 8.dp)
                                    .pointerInput(Unit) {
                                        var accumulatedDrag = 0f
                                        detectDragGesturesAfterLongPress(
                                            onDragStart = { accumulatedDrag = 0f },
                                            onDrag = { change, dragAmount -> 
                                                change.consume()
                                                accumulatedDrag += dragAmount.y
                                                val threshold = 150f
                                                if (accumulatedDrag > threshold && index < fieldOrder.size - 1) {
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index + 1]
                                                    mutableOrder[index + 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                    accumulatedDrag = 0f
                                                } else if (accumulatedDrag < -threshold && index > 0) {
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index - 1]
                                                    mutableOrder[index - 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                    accumulatedDrag = 0f
                                                }
                                            }
                                        )
                                    }
                            )
                        }
                        OutlinedTextField(
                            value = username,
                            onValueChange = { username = it },
                            label = { Text("Username") },
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
                
                if (field == "Password" && showPassword) {
                    var passVisible by remember { mutableStateOf(false) }
                    val strength = when {
                        password.isEmpty() -> 0f
                        password.length < 8 -> 0.25f
                        password.length < 12 -> 0.5f
                        password.length < 16 -> 0.75f
                        else -> 1f
                    }
                    val strengthColor = when {
                        password.isEmpty() -> Color.Transparent
                        password.length < 8 -> Color.Red
                        password.length < 12 -> Color(0xFFFFA500)
                        password.length < 16 -> Color(0xFF9ACD32)
                        else -> Color.Green
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        if (isDeleteMode) {
                            Checkbox(checked = selectedFieldsToDelete.contains("Password"), onCheckedChange = { checked ->
                                if (checked) selectedFieldsToDelete = selectedFieldsToDelete + "Password" else selectedFieldsToDelete = selectedFieldsToDelete - "Password"
                            })
                        }
                        if (isReorderMode) {
                            Icon(
                                Icons.Default.DragHandle, 
                                contentDescription = "Reorder",
                                modifier = Modifier
                                    .padding(end = 8.dp)
                                    .pointerInput(Unit) {
                                        var accumulatedDrag = 0f
                                        detectDragGesturesAfterLongPress(
                                            onDragStart = { accumulatedDrag = 0f },
                                            onDrag = { change, dragAmount -> 
                                                change.consume()
                                                accumulatedDrag += dragAmount.y
                                                val threshold = 150f
                                                if (accumulatedDrag > threshold && index < fieldOrder.size - 1) {
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index + 1]
                                                    mutableOrder[index + 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                    accumulatedDrag = 0f
                                                } else if (accumulatedDrag < -threshold && index > 0) {
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index - 1]
                                                    mutableOrder[index - 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                    accumulatedDrag = 0f
                                                }
                                            }
                                        )
                                    }
                            )
                        }
                        Column(modifier = Modifier.weight(1f)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                OutlinedTextField(
                                    value = password,
                                    onValueChange = { password = it },
                                    label = { Text("Password") },
                                    visualTransformation = if (passVisible) VisualTransformation.None else PasswordVisualTransformation(),
                                    trailingIcon = {
                                        Row {
                                            IconButton(onClick = { showPasswordGenerator = true }) {
                                                Icon(Icons.Default.Build, "Generate Password")
                                            }
                                            IconButton(onClick = { passVisible = !passVisible }) {
                                                Icon(if (passVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, "Toggle Password")
                                            }
                                            IconButton(onClick = { clipboardManager.setText(androidx.compose.ui.text.AnnotatedString(password)) }) {
                                                Icon(Icons.Default.ContentCopy, "Copy Password")
                                            }
                                        }
                                    },
                                    modifier = Modifier.weight(1f)
                                )
                            }
                            if (password.isNotEmpty()) {
                                LinearProgressIndicator(
                                    progress = { strength },
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(horizontal = 8.dp, vertical = 4.dp)
                                        .height(4.dp)
                                        .clip(RoundedCornerShape(2.dp)),
                                    color = strengthColor,
                                    trackColor = MaterialTheme.colorScheme.surfaceVariant,
                                )
                            }
                        }
                    }
                }
                
                if (field == "URL" && showUrl) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        if (isDeleteMode) {
                            Checkbox(checked = selectedFieldsToDelete.contains("URL"), onCheckedChange = { checked ->
                                if (checked) selectedFieldsToDelete = selectedFieldsToDelete + "URL" else selectedFieldsToDelete = selectedFieldsToDelete - "URL"
                            })
                        }
                        if (isReorderMode) {
                            Icon(
                                Icons.Default.DragHandle, 
                                contentDescription = "Reorder",
                                modifier = Modifier
                                    .padding(end = 8.dp)
                                    .pointerInput(Unit) {
                                        var accumulatedDrag = 0f
                                        detectDragGesturesAfterLongPress(
                                            onDragStart = { accumulatedDrag = 0f },
                                            onDrag = { change, dragAmount -> 
                                                change.consume()
                                                accumulatedDrag += dragAmount.y
                                                val threshold = 150f
                                                if (accumulatedDrag > threshold && index < fieldOrder.size - 1) {
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index + 1]
                                                    mutableOrder[index + 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                    accumulatedDrag = 0f
                                                } else if (accumulatedDrag < -threshold && index > 0) {
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index - 1]
                                                    mutableOrder[index - 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                    accumulatedDrag = 0f
                                                }
                                            }
                                        )
                                    }
                            )
                        }
                        OutlinedTextField(
                            value = url,
                            onValueChange = { url = it },
                            label = { Text("URL") },
                            modifier = Modifier.weight(1f)
                        )
                    }
                }
                
                if (field == "Notes" && showNotes) {
                    Row(verticalAlignment = Alignment.Top) {
                        if (isDeleteMode) {
                            Checkbox(checked = selectedFieldsToDelete.contains("Notes"), onCheckedChange = { checked ->
                                if (checked) selectedFieldsToDelete = selectedFieldsToDelete + "Notes" else selectedFieldsToDelete = selectedFieldsToDelete - "Notes"
                            })
                        }
                        if (isReorderMode) {
                            Icon(
                                Icons.Default.DragHandle, 
                                contentDescription = "Reorder",
                                modifier = Modifier
                                    .padding(end = 8.dp)
                                    .pointerInput(Unit) {
                                        var accumulatedDrag = 0f
                                        detectDragGesturesAfterLongPress(
                                            onDragStart = { accumulatedDrag = 0f },
                                            onDrag = { change, dragAmount -> 
                                                change.consume()
                                                accumulatedDrag += dragAmount.y
                                                val threshold = 150f
                                                if (accumulatedDrag > threshold && index < fieldOrder.size - 1) {
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index + 1]
                                                    mutableOrder[index + 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                    accumulatedDrag = 0f
                                                } else if (accumulatedDrag < -threshold && index > 0) {
                                                    val mutableOrder = fieldOrder.toMutableList()
                                                    val temp = mutableOrder[index - 1]
                                                    mutableOrder[index - 1] = mutableOrder[index]
                                                    mutableOrder[index] = temp
                                                    fieldOrder = mutableOrder
                                                    accumulatedDrag = 0f
                                                }
                                            }
                                        )
                                    }
                            )
                        }
                        OutlinedTextField(
                            value = notes,
                            onValueChange = { notes = it },
                            label = { Text("Notes") },
                            modifier = Modifier.weight(1f),
                            minLines = 3
                        )
                    }
                }
            }
            item {
                OutlinedTextField(
                    value = tagsString,
                    onValueChange = { tagsString = it },
                    label = { Text("Tags (comma separated)") },
                    modifier = Modifier.fillMaxWidth()
                )
            }
            items(customFields, key = { it.id }) { field ->
                var isVisible by remember { mutableStateOf(!field.isHidden) }
                Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                    if (isDeleteMode) {
                        Checkbox(
                            checked = selectedFieldsToDelete.contains("Custom:${field.name}"),
                            onCheckedChange = { checked ->
                                val key = "Custom:${field.name}"
                                if (checked) selectedFieldsToDelete = selectedFieldsToDelete + key
                                else selectedFieldsToDelete = selectedFieldsToDelete - key
                            },
                            modifier = Modifier.padding(end = 8.dp)
                        )
                    }
                    OutlinedTextField(
                        value = field.value,
                        onValueChange = { newValue -> 
                            customFields = customFields.map { 
                                if (it.id == field.id) it.copy(value = newValue) else it
                            }
                        },
                        label = { Text(field.name) },
                        visualTransformation = if (!isVisible && field.isHidden) PasswordVisualTransformation() else VisualTransformation.None,
                        trailingIcon = {
                            Row {
                                if (field.isHidden) {
                                    IconButton(onClick = { isVisible = !isVisible }) {
                                        Icon(if (isVisible) Icons.Default.VisibilityOff else Icons.Default.Visibility, contentDescription = "Toggle Visibility")
                                    }
                                }
                                IconButton(onClick = {
                                    customFields = customFields.filter { it.id != field.id }
                                }) {
                                    Icon(Icons.Default.Delete, "Delete")
                                }
                            }
                        },
                        modifier = Modifier.weight(1f),
                        shape = RoundedCornerShape(12.dp)
                    )
                }
            }
            item { Spacer(modifier = Modifier.height(16.dp)) }
        }

        if (showAddFieldDialog) {
            var fieldName by remember { mutableStateOf("") }
            var fieldValue by remember { mutableStateOf("") }
            var isHidden by remember { mutableStateOf(false) }
            var showCopyButton by remember { mutableStateOf(true) } // Assume true for now

            AlertDialog(
                onDismissRequest = { showAddFieldDialog = false },
                title = { Text("Add Custom Field") },
                text = {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        OutlinedTextField(
                            value = fieldName,
                            onValueChange = { fieldName = it },
                            label = { Text("Field Name") },
                            modifier = Modifier.fillMaxWidth()
                        )
                        OutlinedTextField(
                            value = fieldValue,
                            onValueChange = { fieldValue = it },
                            label = { Text("Field Value") },
                            modifier = Modifier.fillMaxWidth()
                        )
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Checkbox(checked = isHidden, onCheckedChange = { isHidden = it })
                            Text("Hidden")
                        }
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Checkbox(checked = showCopyButton, onCheckedChange = { showCopyButton = it })
                            Text("Show Copy Button")
                        }
                    }
                },
                confirmButton = {
                    TextButton(onClick = {
                        if (fieldName.equals("Username", ignoreCase = true) && !showUsername) {
                            showUsername = true
                            username = fieldValue
                        } else if (fieldName.equals("Password", ignoreCase = true) && !showPassword) {
                            showPassword = true
                            password = fieldValue
                        } else if (fieldName.equals("URL", ignoreCase = true) && !showUrl) {
                            showUrl = true
                            url = fieldValue
                        } else if (fieldName.equals("Notes", ignoreCase = true) && !showNotes) {
                            showNotes = true
                            notes = fieldValue
                        } else if (fieldName.isNotBlank()) {
                            customFields = customFields + CustomFieldData(name = fieldName, value = fieldValue, isHidden = isHidden, showCopyButton = showCopyButton)
                        }
                        showAddFieldDialog = false
                    }) { Text("Add") }
                },
                dismissButton = {
                    TextButton(onClick = { showAddFieldDialog = false }) { Text("Cancel") }
                }
            )
        }

        if (showPasswordGenerator) {
            var passLength by remember { mutableStateOf(16f) }
            var useUpper by remember { mutableStateOf(true) }
            var useLower by remember { mutableStateOf(true) }
            var useNumbers by remember { mutableStateOf(true) }
            var useSymbols by remember { mutableStateOf(true) }
            var excludeSimilar by remember { mutableStateOf(false) }
            
            var generatedPassword by remember { mutableStateOf("") }
            
            val strength = when {
                passLength < 8 -> "Weak"
                passLength < 12 -> "Medium"
                passLength < 16 -> "Strong"
                else -> "Excellent"
            }
            
            val strengthColor = when(strength) {
                "Weak" -> androidx.compose.ui.graphics.Color.Red
                "Medium" -> androidx.compose.ui.graphics.Color(0xFFFFA500) // Orange
                "Strong" -> androidx.compose.ui.graphics.Color(0xFF9ACD32) // YellowGreen
                else -> androidx.compose.ui.graphics.Color.Green
            }

            fun generateNewPass() {
                var upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                var lower = "abcdefghijklmnopqrstuvwxyz"
                var numbers = "0123456789"
                var symbols = "!@#$%^&*()-_+="
                if (excludeSimilar) {
                    upper = upper.filter { it !in "IO" }
                    lower = lower.filter { it !in "l1o0" }
                    numbers = numbers.filter { it !in "10" }
                    symbols = symbols.filter { it !in "|I" }
                }
                var chars = ""
                if (useUpper) chars += upper
                if (useLower) chars += lower
                if (useNumbers) chars += numbers
                if (useSymbols) chars += symbols
                if (chars.isEmpty()) chars = lower
                
                var genPass = ""
                for (i in 0 until passLength.toInt()) {
                    genPass += chars.random()
                }
                generatedPassword = genPass
            }
            
            LaunchedEffect(passLength, useUpper, useLower, useNumbers, useSymbols, excludeSimilar) {
                generateNewPass()
            }

            AlertDialog(
                onDismissRequest = { showPasswordGenerator = false },
                title = { Text("Password Generator") },
                text = {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text(generatedPassword, fontSize = 18.sp, fontWeight = FontWeight.Bold, modifier = Modifier.align(Alignment.CenterHorizontally))
                        Text("Length: ${passLength.toInt()}")
                        Slider(
                            value = passLength,
                            onValueChange = { passLength = it },
                            valueRange = 4f..64f
                        )
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Checkbox(checked = useUpper, onCheckedChange = { useUpper = it })
                            Text("Uppercase")
                        }
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Checkbox(checked = useLower, onCheckedChange = { useLower = it })
                            Text("Lowercase")
                        }
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Checkbox(checked = useNumbers, onCheckedChange = { useNumbers = it })
                            Text("Numbers")
                        }
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Checkbox(checked = useSymbols, onCheckedChange = { useSymbols = it })
                            Text("Symbols")
                        }
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Checkbox(checked = excludeSimilar, onCheckedChange = { excludeSimilar = it })
                            Text("Exclude similar characters")
                        }
                        Text("Strength: $strength", color = strengthColor, fontWeight = FontWeight.Bold)
                    }
                },
                confirmButton = {
                    Row {
                        TextButton(onClick = {
                            clipboardManager.setText(AnnotatedString(generatedPassword))
                        }) { Text("Copy") }
                        TextButton(onClick = {
                            password = generatedPassword
                            showPasswordGenerator = false
                        }) { Text("Use Password") }
                    }
                },
                dismissButton = {
                    TextButton(onClick = { showPasswordGenerator = false }) { Text("Cancel") }
                }
            )
        }


        if (showIconDialog) {
            AlertDialog(
                onDismissRequest = { showIconDialog = false },
                title = { Text("Select Icon") },
                text = {
                    LazyVerticalGrid(
                        columns = GridCells.Fixed(4),
                        horizontalArrangement = Arrangement.spacedBy(16.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        items(predefinedIcons) { icon ->
                            Box(
                                modifier = Modifier
                                    .size(48.dp)
                                    .clip(CircleShape)
                                    .background(MaterialTheme.colorScheme.surfaceVariant)
                                    .clickable {
                                        iconName = icon
                                        showIconDialog = false
                                    },
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(parseIcon(icon), contentDescription = icon, tint = parseColor(color))
                            }
                        }
                    }
                },
                confirmButton = {
                    TextButton(onClick = { showIconDialog = false }) { Text("Cancel") }
                }
            )
        }
        if (showColorDialog) {
            var currentHsv by remember {
                mutableStateOf(
                    FloatArray(3).apply {
                        android.graphics.Color.colorToHSV(parseColor(color).toArgb(), this)
                    }
                )
            }
            val currentColor = Color.hsv(currentHsv[0], currentHsv[1], currentHsv[2])

            AlertDialog(
                onDismissRequest = { showColorDialog = false },
                title = { Text("Select Color") },
                text = {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        // Color Wheel
                        BoxWithConstraints(
                            modifier = Modifier
                                .fillMaxWidth()
                                .aspectRatio(1f)
                        ) {
                            val diameter = constraints.maxWidth.toFloat()
                            val radius = diameter / 2f

                            androidx.compose.foundation.Canvas(
                                modifier = Modifier
                                    .fillMaxSize()
                                    .pointerInput(Unit) {
                                        detectDragGestures { change, _ ->
                                            val position = change.position
                                            val dx = position.x - radius
                                            val dy = position.y - radius
                                            val distance = min(sqrt(dx * dx + dy * dy), radius)
                                            var angle = Math.toDegrees(atan2(dy.toDouble(), dx.toDouble())).toFloat()
                                            if (angle < 0) angle += 360f
                                            
                                            currentHsv = floatArrayOf(
                                                angle,
                                                distance / radius,
                                                currentHsv[2]
                                            )
                                        }
                                    }
                                    .pointerInput(Unit) {
                                        detectTapGestures { offset ->
                                            val dx = offset.x - radius
                                            val dy = offset.y - radius
                                            val distance = min(sqrt(dx * dx + dy * dy), radius)
                                            var angle = Math.toDegrees(atan2(dy.toDouble(), dx.toDouble())).toFloat()
                                            if (angle < 0) angle += 360f
                                            
                                            currentHsv = floatArrayOf(
                                                angle,
                                                distance / radius,
                                                currentHsv[2]
                                            )
                                        }
                                    }
                            ) {
                                drawCircle(
                                    brush = androidx.compose.ui.graphics.Brush.sweepGradient(
                                        colors = listOf(
                                            Color.Red,
                                            Color.Yellow,
                                            Color.Green,
                                            Color.Cyan,
                                            Color.Blue,
                                            Color.Magenta,
                                            Color.Red
                                        )
                                    ),
                                    radius = radius
                                )
                                drawCircle(
                                    brush = androidx.compose.ui.graphics.Brush.radialGradient(
                                        colors = listOf(Color.White, Color.Transparent),
                                        radius = radius
                                    ),
                                    radius = radius
                                )
                                // Draw selector
                                val angleRad = Math.toRadians(currentHsv[0].toDouble())
                                val dist = currentHsv[1] * radius
                                val selX = radius + dist * cos(angleRad).toFloat()
                                val selY = radius + dist * sin(angleRad).toFloat()
                                
                                drawCircle(
                                    color = Color.Black,
                                    radius = 12f,
                                    center = androidx.compose.ui.geometry.Offset(selX, selY),
                                    style = androidx.compose.ui.graphics.drawscope.Stroke(width = 4f)
                                )
                                drawCircle(
                                    color = Color.White,
                                    radius = 10f,
                                    center = androidx.compose.ui.geometry.Offset(selX, selY),
                                    style = androidx.compose.ui.graphics.drawscope.Stroke(width = 4f)
                                )
                            }
                        }

                        // Lightness Slider
                        Text("Lightness/Darkness")
                        Slider(
                            value = currentHsv[2],
                            onValueChange = { newValue ->
                                currentHsv = floatArrayOf(currentHsv[0], currentHsv[1], newValue)
                            },
                            valueRange = 0f..1f
                        )
                        
                        // Preview
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .clip(CircleShape)
                                .background(currentColor)
                        )
                    }
                },
                confirmButton = {
                    TextButton(onClick = {
                        color = String.format("#%06X", (0xFFFFFF and currentColor.toArgb()))
                        showColorDialog = false
                    }) { Text("OK") }
                },
                dismissButton = {
                    TextButton(onClick = { showColorDialog = false }) { Text("Cancel") }
                }
            )
        }

        if (showAttachmentsDialog) {
            AlertDialog(
                onDismissRequest = { showAttachmentsDialog = false },
                title = { Text("Attachments") },
                text = {
                    Column {
                        if (attachments.isEmpty()) {
                            Text("No attachments.")
                        }
                        // Mock adding attachment logic
                        Button(onClick = {
                            attachments = attachments + "document_${attachments.size + 1}.pdf"
                        }, modifier = Modifier.padding(top = 16.dp)) {
                            Text("Add File")
                        }
                        Spacer(modifier = Modifier.height(16.dp))
                        attachments.forEach { file ->
                            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(vertical = 4.dp)) {
                                Icon(Icons.AutoMirrored.Filled.InsertDriveFile, "File")
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(file, modifier = Modifier.weight(1f))
                                IconButton(onClick = {
                                    attachments = attachments.filter { it != file }
                                }) {
                                    Icon(Icons.Default.Delete, "Remove")
                                }
                            }
                        }
                    }
                },
                confirmButton = {
                    TextButton(onClick = { showAttachmentsDialog = false }) { Text("Close") }
                }
            )
        }


        if (showTemplateSheet) {
            ModalBottomSheet(
                onDismissRequest = { showTemplateSheet = false },
                sheetState = templateSheetState
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp)
                ) {
                    Text("Select a template", fontSize = 20.sp, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    LazyColumn {
                        items(templates, key = { it.uuid.toString() }) { template ->
                            Card(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 8.dp)
                                    .clickable {
                                        try {
                                            title = template[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: ""
                                            username = template[app.keemobile.kotpass.constants.BasicField.UserName]?.content ?: ""
                                            password = template[app.keemobile.kotpass.constants.BasicField.Password]?.content ?: ""
                                            url = template[app.keemobile.kotpass.constants.BasicField.Url]?.content ?: ""
                                            notes = template[app.keemobile.kotpass.constants.BasicField.Notes]?.content ?: ""
                                            iconName = template.icon.name
                                            color = template.customData["ThemeColor"]?.value ?: "Blue"
                                            tagsString = template.tags.joinToString(", ")
                                            
                                            showUsername = template.customData["Hide_UserName"]?.value != "true"
                                            showPassword = template.customData["Hide_Password"]?.value != "true"
                                            showUrl = template.customData["Hide_Url"]?.value != "true"
                                            showNotes = template.customData["Hide_Notes"]?.value != "true"
                                            
                                            val newCustomFields = mutableListOf<CustomFieldData>()
                                            val basicFields = listOf(app.keemobile.kotpass.constants.BasicField.Title(), app.keemobile.kotpass.constants.BasicField.UserName(), app.keemobile.kotpass.constants.BasicField.Password(), app.keemobile.kotpass.constants.BasicField.Url(), app.keemobile.kotpass.constants.BasicField.Notes())
                                            
                                            for ((key, value) in template.fields) {
                                                if (key !in basicFields && key != "Notes" && key != "Title" && key != "UserName" && key != "URL" && key != "Password") {
                                                    val fieldName = key
                                                    val isHidden = value is app.keemobile.kotpass.models.EntryValue.Encrypted
                                                    val fieldValue = value.content
                                                    val showCopy = template.customData["ShowCopyButton_$fieldName"]?.value == "true"
                                                    newCustomFields.add(CustomFieldData(name = fieldName, value = fieldValue, isHidden = isHidden, showCopyButton = showCopy))
                                                }
                                            }
                                            customFields = newCustomFields
                                            
                                            scope.launch { templateSheetState.hide() }.invokeOnCompletion {
                                                if (!templateSheetState.isVisible) {
                                                    showTemplateSheet = false
                                                }
                                            }
                                        } catch (e: Exception) {
                                            android.util.Log.e("AddEntryScreen", "Failed to apply template")
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
                                    Text(text = template[app.keemobile.kotpass.constants.BasicField.Title]?.content ?: "Unnamed", fontSize = 18.sp)
                                }
                            }
                        }
                    }
                    Spacer(modifier = Modifier.height(32.dp))
                }
            }
        }
    }
}
