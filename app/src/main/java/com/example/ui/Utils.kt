package com.example.ui

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.*
import androidx.compose.material.icons.filled.*
import androidx.compose.runtime.*
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector

@Composable
fun debounced(onClick: () -> Unit): () -> Unit {
    var lastClickTime by remember { mutableStateOf(0L) }
    return {
        val currentTime = System.currentTimeMillis()
        if (currentTime - lastClickTime >= 500L) {
            lastClickTime = currentTime
            onClick()
        }
    }
}

fun parseColor(color: String?): Color {
    return if (color.isNullOrBlank()) {
        Color.White
    } else {
        try {
            val hex = color.replace("#", "").uppercase()
            when (hex.length) {
                6 -> Color(
                    red = hex.substring(0, 2).toInt(16).toFloat() / 255f,
                    green = hex.substring(2, 4).toInt(16).toFloat() / 255f,
                    blue = hex.substring(4, 6).toInt(16).toFloat() / 255f,
                    alpha = 1f
                )
                8 -> Color(
                    red = hex.substring(2, 4).toInt(16).toFloat() / 255f,
                    green = hex.substring(4, 6).toInt(16).toFloat() / 255f,
                    blue = hex.substring(6, 8).toInt(16).toFloat() / 255f,
                    alpha = hex.substring(0, 2).toInt(16).toFloat() / 255f
                )
                else -> Color.White
            }
        } catch (e: Exception) {
            Color.White
        }
    }
}

fun parseIcon(iconName: String): ImageVector {
    return when (iconName.lowercase()) {
        "folder" -> Icons.Default.Folder
        "folder_open" -> Icons.Default.FolderOpen
        "document" -> Icons.Default.Description
        "description" -> Icons.Default.Description
        "password" -> Icons.Default.Lock
        "lock" -> Icons.Default.Lock
        "unlock" -> Icons.Default.LockOpen
        "email" -> Icons.Default.Email
        "mail" -> Icons.Default.Email
        "phone" -> Icons.Default.Phone
        "call" -> Icons.Default.Phone
        "web" -> Icons.Default.Web
        "browser" -> Icons.Default.Web
        "address" -> Icons.Default.LocationOn
        "location" -> Icons.Default.LocationOn
        "note" -> Icons.Default.Note
        "text" -> Icons.Default.Note
        "calendar" -> Icons.Default.CalendarToday
        "date" -> Icons.Default.CalendarToday
        "clock" -> Icons.Default.AccessTime
        "time" -> Icons.Default.AccessTime
        "key" -> Icons.Default.VpnKey
        "user" -> Icons.Default.Person
        "person" -> Icons.Default.Person
        "profile" -> Icons.Default.Person
        "home" -> Icons.Default.Home
        "house" -> Icons.Default.Home
        "settings" -> Icons.Default.Settings
        "security" -> Icons.Default.Security
        "shield" -> Icons.Default.Security
        "wallet" -> Icons.Default.AccountBalanceWallet
        "card" -> Icons.Default.CreditCard
        "credit_card" -> Icons.Default.CreditCard
        "id" -> Icons.Default.Badge
        "badge" -> Icons.Default.Badge
        "passport" -> Icons.Default.Badge
        "license" -> Icons.Default.DriveFileRenameOutline
        "certificate" -> Icons.Default.LocalLibrary
        "ticket" -> Icons.Default.ConfirmReservation
        "membership" -> Icons.Default.Group
        "group" -> Icons.Default.Group
        "insurance" -> Icons.Default.LocalInsurance
        "medical" -> Icons.Default.LocalHospital
        "hospital" -> Icons.Default.LocalHospital
        "emergency" -> Icons.Default.ReportEmergency
        "crypto" -> Icons.Default.AccountBalance
        "bitcoin" -> Icons.Default.AccountBalanceWallet
        "ethereum" -> Icons.Default.AccountBalance
        "other" -> Icons.Default.Help
        "help" -> Icons.Default.Help
        "info" -> Icons.Default.Info
        "warning" -> Icons.Default.Warning
        "error" -> Icons.Default.Error
        "success" -> Icons.Default.CheckCircle
        "check" -> Icons.Default.CheckCircle
        "edit" -> Icons.Default.Edit
        "pencil" -> Icons.Default.Edit
        "delete" -> Icons.Default.Delete
        "remove" -> Icons.Default.Delete
        "add" -> Icons.Default.Add
        "create" -> Icons.Default.Add
        "new" -> Icons.Default.Add
        "save" -> Icons.Default.Save
        "copy" -> Icons.Default.ContentCopy
        "paste" -> Icons.Default.ContentPaste
        "cut" -> Icons.Default.ContentCut
        "search" -> Icons.Default.Search
        "find" -> Icons.Default.Search
        "filter" -> Icons.Default.FilterList
        "sort" -> Icons.Default.Sort
        "share" -> Icons.Default.Share
        "send" -> Icons.Default.Send
        "receive" -> Icons.Default.Inbox
        "inbox" -> Icons.Default.Inbox
        "outbox" -> Icons.Default.Outbox
        "upload" -> Icons.Default.CloudUpload
        "download" -> Icons.Default.CloudDownload
        "cloud" -> Icons.Default.Cloud
        "sync" -> Icons.Default.Sync
        "refresh" -> Icons.Default.Refresh
        "undo" -> Icons.Default.Undo
        "redo" -> Icons.Default.Redo
        "back" -> Icons.Default.ArrowBack
        "forward" -> Icons.Default.ArrowForward
        "up" -> Icons.Default.ArrowUpward
        "down" -> Icons.Default.ArrowDownward
        "left" -> Icons.Default.ArrowLeft
        "right" -> Icons.Default.ArrowRight
        "menu" -> Icons.Default.Menu
        "more" -> Icons.Default.MoreVert
        "more_vert" -> Icons.Default.MoreVert
        "close" -> Icons.Default.Close
        "cancel" -> Icons.Default.Close
        "done" -> Icons.Default.Done
        "ok" -> Icons.Default.Done
        "check" -> Icons.Default.CheckCircle
        "clear" -> Icons.Default.Clear
        "print" -> Icons.Default.Print
        "scan" -> Icons.Default.Scan
        "qr" -> Icons.Default.QrCode
        "barcode" -> Icons.Default.Barcode
        "camera" -> Icons.Default.Camera
        "image" -> Icons.Default.Image
        "photo" -> Icons.Default.Image
        "video" -> Icons.Default.Video
        "music" -> Icons.Default.MusicNote
        "audio" -> Icons.Default.MusicNote
        "mic" -> Icons.Default.Mic
        "volume" -> Icons.Default.VolumeUp
        "mute" -> Icons.Default.VolumeOff
        "wifi" -> Icons.Default.Wifi
        "signal" -> Icons.Default.SignalWifi
        "battery" -> Icons.Default.BatteryFull
        "power" -> Icons.Default.Power
        "lock" -> Icons.Default.Lock
        "unlock" -> Icons.Default.LockOpen
        "private" -> Icons.Default.Lock
        "public" -> Icons.Default.Public
        "star" -> Icons.Default.Star
        "favorite" -> Icons.Default.Favorite
        "like" -> Icons.Default.ThumbUp
        "dislike" -> Icons.Default.ThumbDown
        "thumb_up" -> Icons.Default.ThumbUp
        "thumb_down" -> Icons.Default.ThumbDown
        "heart" -> Icons.Default.Favorite
        "love" -> Icons.Default.Favorite
        "tag" -> Icons.Default.LocalOffer
        "label" -> Icons.Default.Label
        "category" -> Icons.Default.Category
        "type" -> Icons.Default.Category
        "kind" -> Icons.Default.Category
        else -> Icons.Default.Folder
    }
}
