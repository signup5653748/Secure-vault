package com.example.data

import android.content.Context
import android.net.Uri
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import app.keemobile.kotpass.database.KeePassDatabase
import app.keemobile.kotpass.database.Credentials
import app.keemobile.kotpass.cryptography.EncryptedValue
import app.keemobile.kotpass.models.Meta
import app.keemobile.kotpass.database.decode
import app.keemobile.kotpass.database.encode

object KeePassHelper {
    suspend fun loadDatabase(context: Context, uri: Uri, password: String): KeePassDatabase? {
        return withContext(Dispatchers.IO) {
            try {
                val credentials = Credentials.from(EncryptedValue.fromString(password))
                context.contentResolver.openInputStream(uri)?.use { inputStream ->
                    KeePassDatabase.decode(inputStream, credentials)
                }
            } catch (e: Exception) {
                e.printStackTrace()
                null
            }
        }
    }

    suspend fun createNewDatabase(context: Context, uri: Uri, password: String): Pair<Boolean, String?> {
        return withContext(Dispatchers.IO) {
            try {
                val credentials = Credentials.from(EncryptedValue.fromString(password))
                val db = KeePassDatabase.Ver4x.create("Root", Meta(), credentials)
                
                context.contentResolver.openOutputStream(uri)?.use { outputStream ->
                    db.encode(outputStream)
                    Pair(true, null)
                } ?: Pair(false, "Failed to open output stream")
            } catch (e: Throwable) {
                e.printStackTrace()
                Pair(false, e.stackTraceToString())
            }
        }
    }
}
