package com.example.data

import android.content.Context
import android.content.SharedPreferences
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class SettingsRepository(context: Context) {
    private val prefs: SharedPreferences = context.getSharedPreferences("app_settings", Context.MODE_PRIVATE)

    private val _themeColor = MutableStateFlow(prefs.getString("theme_color", "Blue") ?: "Blue")
    val themeColor: StateFlow<String> = _themeColor.asStateFlow()

    private val _textSizeMultiplier = MutableStateFlow(prefs.getFloat("text_size_multiplier", 1.0f))
    val textSizeMultiplier: StateFlow<Float> = _textSizeMultiplier.asStateFlow()

    private val _openFromFileManager = MutableStateFlow(prefs.getBoolean("open_from_file_manager", true))
    val openFromFileManager: StateFlow<Boolean> = _openFromFileManager.asStateFlow()

    private val _databaseUri = MutableStateFlow(prefs.getString("database_uri", null))
    val databaseUri: StateFlow<String?> = _databaseUri.asStateFlow()

    
    private val _lockOnBackground = MutableStateFlow(prefs.getBoolean("lock_on_background", true))
    val lockOnBackground: StateFlow<Boolean> = _lockOnBackground.asStateFlow()

    private val _clipboardAutoClear = MutableStateFlow(prefs.getBoolean("clipboard_auto_clear", true))
    val clipboardAutoClear: StateFlow<Boolean> = _clipboardAutoClear.asStateFlow()

    private val _enableBiometrics = MutableStateFlow(prefs.getBoolean("enable_biometrics", false))
    val enableBiometrics: StateFlow<Boolean> = _enableBiometrics.asStateFlow()

    fun setLockOnBackground(enabled: Boolean) {
        prefs.edit().putBoolean("lock_on_background", enabled).apply()
        _lockOnBackground.value = enabled
    }

    fun setClipboardAutoClear(enabled: Boolean) {
        prefs.edit().putBoolean("clipboard_auto_clear", enabled).apply()
        _clipboardAutoClear.value = enabled
    }

    fun setEnableBiometrics(enabled: Boolean) {
        prefs.edit().putBoolean("enable_biometrics", enabled).apply()
        _enableBiometrics.value = enabled
    }

    fun setThemeColor(color: String) {
        prefs.edit().putString("theme_color", color).apply()
        _themeColor.value = color
    }

    fun setTextSizeMultiplier(multiplier: Float) {
        prefs.edit().putFloat("text_size_multiplier", multiplier).apply()
        _textSizeMultiplier.value = multiplier
    }

    fun setOpenFromFileManager(enabled: Boolean) {
        prefs.edit().putBoolean("open_from_file_manager", enabled).apply()
        _openFromFileManager.value = enabled
    }

    fun setDatabaseUri(uri: String?) {
        prefs.edit().putString("database_uri", uri).apply()
        _databaseUri.value = uri
    }

    fun clearAll() {
        prefs.edit().clear().apply()
        _themeColor.value = "Blue"
        _textSizeMultiplier.value = 1.0f
        _openFromFileManager.value = true
        _databaseUri.value = null
        _lockOnBackground.value = true
        _clipboardAutoClear.value = true
        _enableBiometrics.value = false
    }
}