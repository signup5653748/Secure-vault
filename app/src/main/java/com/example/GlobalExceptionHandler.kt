package com.example

import android.app.Activity
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Environment
import android.provider.MediaStore
import android.util.Log
import androidx.core.content.ContextCompat
import java.io.File
import java.io.FileOutputStream
import java.io.OutputStream
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class GlobalExceptionHandler(private val context: Context) : Thread.UncaughtExceptionHandler {
    private val defaultHandler: Thread.UncaughtExceptionHandler? = Thread.getDefaultUncaughtExceptionHandler()

    override fun uncaughtException(thread: Thread, exception: Throwable) {
        val fullTrace = getFullStackTrace(exception)
        
        // Save crash log to Downloads folder
        saveCrashLogToDownloads(fullTrace)
        
        // Show crash dialog to user (start Activity on new task)
        showCrashDialog(fullTrace)
        
        // Let default handler finish the process
        defaultHandler?.uncaughtException(thread, exception)
    }

    private fun getFullStackTrace(throwable: Throwable): String {
        val sb = StringBuilder()
        sb.append("=== SecureVault Crash Report ===\n")
        sb.append("Time: ").append(SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault()).format(Date())).append("\n")
        sb.append("Android: ").append(Build.VERSION.RELEASE).append(" (API ").append(Build.VERSION.SDK_INT).append(")\n")
        sb.append("Device: ").append(Build.MANUFACTURER).append(" ").append(Build.MODEL).append("\n")
        sb.append("App Version: ").append(getAppVersionName()).append("\n\n")
        
        var current: Throwable? = throwable
        var first = true
        while (current != null) {
            if (first) {
                sb.append("Exception: ").append(current.javaClass.name).append(": ").append(current.message).append("\n")
                first = false
            } else {
                sb.append("\nCaused by: ").append(current.javaClass.name).append(": ").append(current.message).append("\n")
            }
            for (element in current.stackTrace) {
                sb.append("  at ")
                    .append(element.className)
                    .append(".")
                    .append(element.methodName)
                    .append("(")
                    .append(element.fileName ?: "Unknown")
                    .append(":")
                    .append(element.lineNumber)
                    .append(")\n")
            }
            current = current.cause
        }
        return sb.toString()
    }

    private fun getAppVersionName(): String {
        return try {
            context.packageManager.getPackageInfo(context.packageName, 0).versionName
        } catch (e: PackageManager.NameNotFoundException) {
            null
        } ?: "unknown"
    }

    private fun saveCrashLogToDownloads(crashLog: String) {
        val fileName = "SecureVault_Crash_Log_${SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(Date())}.txt"
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            // Android 10+: Use MediaStore (scoped storage)
            saveViaMediaStore(fileName, crashLog)
        } else {
            // Android 9 and below: Use legacy file API
            saveViaLegacyApi(fileName, crashLog)
        }
    }

    private fun saveViaMediaStore(fileName: String, content: String) {
        try {
            val resolver = context.contentResolver
            val contentValues = android.content.ContentValues().apply {
                put(MediaStore.MediaColumns.DISPLAY_NAME, fileName)
                put(MediaStore.MediaColumns.MIME_TYPE, "text/plain")
                put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS)
            }
            val uri: Uri? = resolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, contentValues)
            uri?.let { uri ->
                resolver.openOutputStream(uri)?.use { outputStream ->
                    outputStream.write(content.toByteArray())
                }
                Log.i("GlobalExceptionHandler", "Crash log saved to Downloads: $uri")
            }
        } catch (e: Exception) {
            Log.e("GlobalExceptionHandler", "Failed to save crash log via MediaStore", e)
            // Fallback to app-specific external files dir
            saveToAppExternalFiles(fileName, content)
        }
    }

    private fun saveViaLegacyApi(fileName: String, content: String) {
        try {
            val downloadsDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
            if (!downloadsDir.exists()) {
                downloadsDir.mkdirs()
            }
            val file = File(downloadsDir, fileName)
            FileOutputStream(file).use { outputStream ->
                outputStream.write(content.toByteArray())
            }
            Log.i("GlobalExceptionHandler", "Crash log saved to Downloads: ${file.absolutePath}")
        } catch (e: Exception) {
            Log.e("GlobalExceptionHandler", "Failed to save crash log via legacy API", e)
            saveToAppExternalFiles(fileName, content)
        }
    }

    private fun saveToAppExternalFiles(fileName: String, content: String) {
        try {
            val dir = context.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS)
            dir?.let { dir ->
                val file = File(dir, fileName)
                FileOutputStream(file).use { outputStream ->
                    outputStream.write(content.toByteArray())
                }
                Log.i("GlobalExceptionHandler", "Crash log saved to app external files: ${file.absolutePath}")
            }
        } catch (e: Exception) {
            Log.e("GlobalExceptionHandler", "Failed to save crash log to app external files", e)
        }
    }

    private fun showCrashDialog(crashLog: String) {
        try {
            val intent = Intent(context, CrashDialogActivity::class.java).apply {
                putExtra("crash_log", crashLog)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK)
            }
            context.startActivity(intent)
        } catch (e: Exception) {
            Log.e("GlobalExceptionHandler", "Failed to start crash dialog activity", e)
        }
    }

    companion object {
        fun clearCrashLogs(context: Context) {
            context.getSharedPreferences("crash_logs", Context.MODE_PRIVATE)
                .edit()
                .clear()
                .apply()
        }
    }
}

// Separate Activity to show the crash dialog
class CrashDialogActivity : Activity() {
    override fun onCreate(savedInstanceState: android.os.Bundle?) {
        super.onCreate(savedInstanceState)
        
        val crashLog = intent.getStringExtra("crash_log") ?: "No crash details available"
        
        AlertDialog.Builder(this)
            .setTitle("App Crashed")
            .setMessage("The app encountered an error. The details have been saved to your Downloads folder as SecureVault_Crash_Log.txt")
            .setPositiveButton("OK") { _, _ ->
                finishAndRemoveTask()
                android.os.Process.killProcess(android.os.Process.myPid())
                System.exit(1)
            }
            .setCancelable(false)
            .show()
    }
}