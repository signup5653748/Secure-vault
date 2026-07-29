package com.example.ui

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector

fun parseColor(colorString: String?): Color {
    if (colorString == null) return Color.Gray
    return when(colorString.lowercase()) {
        "blue" -> Color.Blue
        "red" -> Color.Red
        "green" -> Color.Green
        "yellow" -> Color.Yellow
        "cyan" -> Color.Cyan
        "magenta" -> Color.Magenta
        "gray" -> Color.Gray
        "black" -> Color.Black
        "white" -> Color.White
        else -> try { Color(android.graphics.Color.parseColor(colorString)) } catch (e: Exception) { Color.Magenta }
    }
}

fun parseIcon(iconName: String?): ImageVector {
    if (iconName == null) return Icons.Default.VpnKey
    return when (iconName) {
        "Key" -> Icons.Default.VpnKey
        "Folder" -> Icons.Default.Folder
        "Network" -> Icons.Default.NetworkWifi
        "Lock" -> Icons.Default.Lock
        "Email" -> Icons.Default.Email
        else -> Icons.Default.VpnKey
    }
}
