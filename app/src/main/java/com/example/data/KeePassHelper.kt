package com.example.data

import android.content.Context
import android.net.Uri
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.linguafranca.pwdb.kdbx.KdbxCredentials
import org.linguafranca.pwdb.kdbx.dom.DomDatabaseWrapper
import java.io.File
import java.io.InputStream

object KeePassHelper {
    suspend fun copyToInternalStorage(context: Context, uri: Uri): File? {
        return withContext(Dispatchers.IO) {
            try {
                val inputStream = context.contentResolver.openInputStream(uri) ?: return@withContext null
                val file = File(context.filesDir, "keepass.kdbx")
                file.outputStream().use { outputStream ->
                    inputStream.copyTo(outputStream)
                }
                file
            } catch (e: Exception) {
                e.printStackTrace()
                null
            }
        }
    }

    suspend fun loadDatabase(file: File, password: String): DomDatabaseWrapper? {
        return withContext(Dispatchers.IO) {
            try {
                val credentials = KdbxCredentials.Password(password.toByteArray())
                DomDatabaseWrapper.load(credentials, file.inputStream()) as DomDatabaseWrapper
            } catch (e: Exception) {
                e.printStackTrace()
                null
            }
        }
    }
}
