import re

with open('/app/applet/app/src/main/java/com/example/data/SettingsRepository.kt', 'r') as f:
    content = f.read()

new_fields = """
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
"""

content = content.replace("fun setThemeColor", new_fields + "\n    fun setThemeColor")

with open('/app/applet/app/src/main/java/com/example/data/SettingsRepository.kt', 'w') as f:
    f.write(content)

