package com.example

import android.content.Context
import android.widget.Toast
import java.io.PrintWriter
import java.io.StringWriter

class GlobalExceptionHandler(private val context: Context) : Thread.UncaughtExceptionHandler {
    private val defaultHandler: Thread.UncaughtExceptionHandler? = Thread.getDefaultUncaughtExceptionHandler()

    override fun uncaughtException(thread: Thread, exception: Throwable) {
        val sw = StringWriter()
        exception.printStackTrace(PrintWriter(sw))
        val stackTrace = sw.toString()
        
        // Save to SharedPreferences so we can read it next launch
        context.getSharedPreferences("crash_logs", Context.MODE_PRIVATE)
            .edit()
            .putString("last_crash", stackTrace)
            .apply()
            
        defaultHandler?.uncaughtException(thread, exception)
    }
}
