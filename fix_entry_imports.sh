#!/bin/bash
sed -i '/import androidx.compose.ui.text.input.VisualTransformation/a \
import androidx.compose.foundation.gestures.detectDragGestures\n\
import androidx.compose.foundation.gestures.detectTapGestures\n\
import kotlin.math.min\n\
import kotlin.math.sqrt\n\
import kotlin.math.atan2\n\
import kotlin.math.cos\n\
import kotlin.math.sin\n\
import androidx.compose.ui.input.pointer.pointerInput\n\
import androidx.compose.ui.graphics.toArgb\n\
import androidx.compose.foundation.shape.CircleShape\n\
import androidx.compose.foundation.lazy.grid.GridCells\n\
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid\n\
import androidx.compose.foundation.lazy.grid.items' app/src/main/java/com/example/ui/AddEntryScreen.kt
