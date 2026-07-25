package com.example

import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.linguafranca.pwdb.kdbx.simple.SimpleDatabase
import java.io.ByteArrayOutputStream
import org.linguafranca.pwdb.kdbx.KdbxCredentials
import java.io.ByteArrayInputStream

@RunWith(RobolectricTestRunner::class)
class TestSimpleRobolectric {
    @Test
    fun testCreate() {
        try {
            val db = SimpleDatabase()
            val out = ByteArrayOutputStream()
            val cred = KdbxCredentials.Password("test".toByteArray())
            db.save(cred, out)
            println("Test passed")
        } catch (e: Exception) {
            e.printStackTrace()
            throw e
        }
    }
}
