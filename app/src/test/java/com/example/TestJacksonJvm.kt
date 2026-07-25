package com.example

import org.junit.Test
import org.junit.runner.RunWith
import org.junit.runners.JUnit4
import org.linguafranca.pwdb.kdbx.jackson.JacksonDatabase
import java.io.ByteArrayOutputStream
import org.linguafranca.pwdb.kdbx.KdbxCredentials
import java.io.ByteArrayInputStream

@RunWith(JUnit4::class)
class TestJacksonJvm {
    @Test
    fun testCreate() {
        try {
            val db = JacksonDatabase()
            val out = ByteArrayOutputStream()
            val cred = KdbxCredentials.Password("test".toByteArray())
            db.save(cred, out)
            println("Jackson test passed!")
        } catch (e: Exception) {
            e.printStackTrace()
            throw e
        }
    }
}
