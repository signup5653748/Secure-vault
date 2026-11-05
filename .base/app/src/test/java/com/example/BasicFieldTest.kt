package com.example

import org.junit.Test
import app.keemobile.kotpass.constants.BasicField

class BasicFieldTest {
    @Test
    fun testBasicField() {
        println(BasicField.Title())
        println(BasicField.UserName())
        println(BasicField.Password())
        println(BasicField.Url())
        println(BasicField.Notes())
    }
}
