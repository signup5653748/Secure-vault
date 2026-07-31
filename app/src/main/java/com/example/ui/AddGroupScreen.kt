package com.example.ui
import androidx.compose.ui.graphics.toArgb
import androidx.compose.foundation.gestures.detectDragGestures

import androidx.compose.foundation.gestures.detectTapGestures

import kotlin.math.min

import kotlin.math.sqrt

import kotlin.math.atan2

import kotlin.math.cos

import kotlin.math.sin

import androidx.compose.ui.input.pointer.pointerInput










import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Palette
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.example.viewmodel.KeePassViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AddGroupScreen(
    viewModel: KeePassViewModel,
    onNavigateBack: () -> Unit,
    isEdit: Boolean = false
) {
    val currentGroup by viewModel.currentGroup.collectAsState()
    var title by remember { mutableStateOf(if (isEdit && currentGroup != null) currentGroup!!.name else "") }
    var iconName by remember { mutableStateOf(if (isEdit && currentGroup != null) currentGroup!!.icon.name else "Folder") }
    var color by remember { mutableStateOf(if (isEdit && currentGroup != null) currentGroup!!.customData["ThemeColor"]?.value ?: "Blue" else "Blue") }
    
    var showIconDialog by remember { mutableStateOf(false) }
    var isSaving by remember { mutableStateOf(false) }
    var showColorDialog by remember { mutableStateOf(false) }
    
    val predefinedIcons = listOf("Folder", "Key", "Network", "Lock", "Email", "World", "Money", "Note")
    val predefinedColors = listOf("Blue", "Red", "Green", "Yellow", "Cyan", "Magenta", "Gray", "Black", "White")
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("New Group") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        },
        bottomBar = {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalArrangement = Arrangement.End,
                verticalAlignment = Alignment.CenterVertically
            ) {
                FloatingActionButton(
                    onClick = {
                        if (!isSaving) {
                            isSaving = true
                            if (isEdit && currentGroup != null) { viewModel.updateGroup(currentGroup!!, title, iconName, color) } else { viewModel.createGroup(title, iconName, color) }
                            onNavigateBack()
                        }
                    },
                    containerColor = Color(0xFF0066FF),
                    contentColor = Color.White,
                    shape = RoundedCornerShape(16.dp),
                    modifier = Modifier.size(56.dp)
                ) {
                    Icon(Icons.Default.Check, contentDescription = "Save")
                }
            }
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Center,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Spacer(modifier = Modifier.width(48.dp)) // balance the palette icon
                Box(
                    modifier = Modifier
                        .size(80.dp)
                        .clip(CircleShape)
                        .background(MaterialTheme.colorScheme.surfaceVariant)
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
            
            Spacer(modifier = Modifier.height(16.dp))
            
            OutlinedTextField(
                value = title,
                onValueChange = { title = it },
                label = { Text("Title") },
                modifier = Modifier.fillMaxWidth()
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
    }
}
