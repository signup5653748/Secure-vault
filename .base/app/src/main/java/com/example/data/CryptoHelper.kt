package com.example.data

import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

object CryptoHelper {
    private const val PREFS_NAME = "secure_prefs"
    private const val KEY_PASSWORD = "master_password"

    private var prefs: android.content.SharedPreferences? = null

    @Synchronized
    private fun getPrefs(context: Context): android.content.SharedPreferences {
        if (prefs == null) {
            val masterKey = MasterKey.Builder(context.applicationContext)
                .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
                .build()
            
            prefs = EncryptedSharedPreferences.create(
                context.applicationContext,
                PREFS_NAME,
                masterKey,
                EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
                EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
            )
        }
        return prefs!!
    }

    fun savePassword(context: Context, password: String) {
        getPrefs(context).edit().putString(KEY_PASSWORD, password).apply()
    }

    fun getPassword(context: Context): String? {
        return getPrefs(context).getString(KEY_PASSWORD, null)
    }
    
    fun clearPassword(context: Context) {
        getPrefs(context).edit().remove(KEY_PASSWORD).apply()
    }
}
