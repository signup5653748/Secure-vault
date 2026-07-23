package com.example.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext

private val DarkBlueColorScheme =
  darkColorScheme(
    primary = Blue40,
    secondary = BlueGrey40,
    tertiary = LightBlue40,
    surfaceVariant = DarkSurface,
    background = DarkBackground,
    surface = DarkSurface
  )

private val DarkGreenColorScheme =
  darkColorScheme(
    primary = Green40,
    secondary = GreenGrey40,
    tertiary = Green40,
    surfaceVariant = DarkSurface,
    background = DarkBackground,
    surface = DarkSurface
  )

private val DarkPurpleColorScheme =
  darkColorScheme(
    primary = Purple40,
    secondary = PurpleGrey40,
    tertiary = Purple40,
    surfaceVariant = DarkSurface,
    background = DarkBackground,
    surface = DarkSurface
  )

private val DarkOrangeColorScheme =
  darkColorScheme(
    primary = Orange40,
    secondary = OrangeGrey40,
    tertiary = Orange40,
    surfaceVariant = DarkSurface,
    background = DarkBackground,
    surface = DarkSurface
  )

@Composable
fun MyApplicationTheme(
  themeColorName: String = "Blue",
  textSizeMultiplier: Float = 1.0f,
  content: @Composable () -> Unit,
) {
  val colorScheme = when (themeColorName) {
      "Green" -> DarkGreenColorScheme
      "Purple" -> DarkPurpleColorScheme
      "Orange" -> DarkOrangeColorScheme
      "Dynamic" -> {
          if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
              dynamicDarkColorScheme(LocalContext.current)
          } else {
              DarkBlueColorScheme
          }
      }
      else -> DarkBlueColorScheme
  }

  MaterialTheme(
      colorScheme = colorScheme, 
      typography = getTypography(textSizeMultiplier), 
      content = content
  )
}
