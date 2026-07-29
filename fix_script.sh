#!/bin/bash

# Remove the bad import
sed -i '/import androidx.compose.ui.graphics.toArgb/d' app/src/main/java/com/example/ui/AddGroupScreen.kt

# Insert properly after package
sed -i '/package com.example.ui/a \
import androidx.compose.ui.graphics.toArgb\n\
import androidx.compose.foundation.gestures.detectDragGestures\n\
import androidx.compose.foundation.gestures.detectTapGestures\n\
import kotlin.math.min\n\
import kotlin.math.max\n\
import kotlin.math.sqrt\n\
import kotlin.math.atan2\n\
import kotlin.math.cos\n\
import kotlin.math.sin\n\
import androidx.compose.ui.input.pointer.pointerInput' app/src/main/java/com/example/ui/AddGroupScreen.kt

# Fix the method calls to use imported ones
sed -i 's/androidx.compose.foundation.gestures.detectDragGestures/detectDragGestures/g' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i 's/androidx.compose.foundation.gestures.detectTapGestures/detectTapGestures/g' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i 's/androidx.compose.ui.input.pointer.pointerInput/pointerInput/g' app/src/main/java/com/example/ui/AddGroupScreen.kt

# Fix math
sed -i 's/kotlin.math.min/min/g' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i 's/kotlin.math.sqrt/sqrt/g' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i 's/kotlin.math.atan2/atan2/g' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i 's/kotlin.math.cos/cos/g' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i 's/kotlin.math.sin/sin/g' app/src/main/java/com/example/ui/AddGroupScreen.kt

# Also fix the `dx * dx + dy * dy` to make sure we pass Float to sqrt
sed -i 's/sqrt(dx \* dx + dy \* dy)/sqrt(dx \* dx + dy \* dy)/g' app/src/main/java/com/example/ui/AddGroupScreen.kt
