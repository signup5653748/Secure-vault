package com.example.ui

import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb

fun test() {
    val c = Color.hsv(180f, 1f, 1f)
    val hex = String.format("#%06X", (0xFFFFFF and c.toArgb()))
    println(hex)
}
