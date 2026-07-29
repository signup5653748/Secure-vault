#!/bin/bash
# Remove all bad imports
sed -i '/import detectDragGestures/d' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i '/import detectTapGestures/d' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i '/import min/d' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i '/import kotlin.math.max/d' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i '/import sqrt/d' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i '/import atan2/d' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i '/import cos/d' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i '/import sin/d' app/src/main/java/com/example/ui/AddGroupScreen.kt
sed -i '/import pointerInput/d' app/src/main/java/com/example/ui/AddGroupScreen.kt

# Insert proper imports
sed -i '/import androidx.compose.ui.graphics.toArgb/a \
import androidx.compose.foundation.gestures.detectDragGestures\n\
import androidx.compose.foundation.gestures.detectTapGestures\n\
import kotlin.math.min\n\
import kotlin.math.sqrt\n\
import kotlin.math.atan2\n\
import kotlin.math.cos\n\
import kotlin.math.sin\n\
import androidx.compose.ui.input.pointer.pointerInput' app/src/main/java/com/example/ui/AddGroupScreen.kt

