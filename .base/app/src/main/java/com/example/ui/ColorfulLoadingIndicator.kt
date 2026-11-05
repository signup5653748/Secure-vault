package com.example.ui

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.dp
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin

@Composable
fun ColorfulLoadingIndicator(modifier: Modifier = Modifier) {
    val infiniteTransition = rememberInfiniteTransition(label = "loading_transition")
    val angle by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 360f,
        animationSpec = infiniteRepeatable(
            animation = tween(1000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "loading_angle"
    )

    val colorIndex by infiniteTransition.animateFloat(
        initialValue = 0f,
        targetValue = 4f,
        animationSpec = infiniteRepeatable(
            animation = tween(2000, easing = LinearEasing),
            repeatMode = RepeatMode.Restart
        ),
        label = "loading_color"
    )

    val colors = listOf(
        Color(0xFF4285F4), // Google Blue
        Color(0xFF34A853), // Google Green
        Color(0xFFFBBC05), // Google Yellow
        Color(0xFFEA4335), // Google Red
        Color(0xFF4285F4)  // Back to Blue
    )

    Canvas(modifier = modifier.size(64.dp)) {
        val sweepAngle = 270f
        val strokeWidth = 6.dp.toPx()
        val radius = size.minDimension / 2 - strokeWidth / 2
        val center = Offset(size.width / 2, size.height / 2)
        
        val currentIndex = colorIndex.toInt() % 4
        val nextIndex = (currentIndex + 1) % 4
        val fraction = colorIndex - currentIndex
        
        val currentColor = androidx.compose.ui.graphics.lerp(colors[currentIndex], colors[nextIndex], fraction)

        drawArc(
            color = currentColor,
            startAngle = angle,
            sweepAngle = sweepAngle,
            useCenter = false,
            topLeft = Offset(center.x - radius, center.y - radius),
            size = Size(radius * 2, radius * 2),
            style = Stroke(width = strokeWidth, cap = StrokeCap.Round)
        )
    }
}
