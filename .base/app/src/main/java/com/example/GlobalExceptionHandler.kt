package com.example

import android.content.Context
import android.widget.Toast
import java.io.PrintWriter
import java.io.StringWriter

class GlobalExceptionHandler(private val context: Context) : Thread.UncaughtExceptionHandler {
    private val defaultHandler: Thread.UncaughtExceptionHandler? = Thread.getDefaultUncaughtExceptionHandler()

    override fun uncaughtException(thread: Thread, exception: Throwable) {
        val sanitizedTrace = sanitizeException(exception)
        
        // Save sanitized crash log without sensitive messages, parameters, or file URIs
        context.getSharedPreferences("crash_logs", Context.MODE_PRIVATE)
            .edit()
            .putString("last_crash", sanitizedTrace)
            .apply()
            
        defaultHandler?.uncaughtException(thread, exception)
    }

    private fun sanitizeException(throwable: Throwable): String {
        val sb = StringBuilder()
        sb.append(throwable.javaClass.name).append("\n")
        for (element in throwable.stackTrace) {
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
        val cause = throwable.cause
        if (cause != null) {
            sb.append("Caused by: ").append(cause.javaClass.name).append("\n")
            for (element in cause.stackTrace) {
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
        }
        return sb.toString()
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
