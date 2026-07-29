package com.example.ui

import androidx.compose.ui.graphics.Color

fun main() {
    val s = "#ff0000"
    val intColor = android.graphics.Color.parseColor(s)
    println("Color int: $intColor")
}
