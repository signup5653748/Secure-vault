package com.example.ui

import androidx.compose.runtime.*

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
