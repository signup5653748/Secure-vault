package com.example

import com.example.data.OtpConfig
import com.example.data.OtpGenerator
import com.example.data.OtpParser
import dev.turingcomplete.kotlinonetimepassword.HmacAlgorithm
import org.junit.Assert.*
import org.junit.Test
import java.time.Clock
import java.time.Instant
import java.time.ZoneOffset

class OtpTest {

    @Test
    fun testBase32Validation() {
        assertTrue(OtpParser.isValidBase32("JBSWY3DPEHPK3PXP"))
        assertTrue(OtpParser.isValidBase32("jbswy 3dpeh-pk3pxp"))
        assertTrue(OtpParser.isValidBase32("MZXW6YTBOI======"))
        assertFalse(OtpParser.isValidBase32("INVALID189!"))
        assertFalse(OtpParser.isValidBase32(""))
        assertFalse(OtpParser.isValidBase32("123890"))
    }

    @Test
    fun testParseOtpAuthUri() {
        val uri = "otpauth://totp/GitHub:octocat?secret=JBSWY3DPEHPK3PXP&issuer=GitHub&algorithm=SHA1&digits=6&period=30"
        val config = OtpParser.parse(uri)

        assertNotNull(config)
        assertEquals("JBSWY3DPEHPK3PXP", config!!.secret)
        assertEquals("GitHub", config.issuer)
        assertEquals("octocat", config.account)
        assertEquals(6, config.digits)
        assertEquals(30L, config.period)
        assertEquals(HmacAlgorithm.SHA1, config.algorithm)
    }

    @Test
    fun testParseRawBase32Secret() {
        val rawSecret = "JBSWY3DPEHPK3PXP"
        val config = OtpParser.parse(rawSecret)

        assertNotNull(config)
        assertEquals("JBSWY3DPEHPK3PXP", config!!.secret)
        assertEquals(6, config.digits)
        assertEquals(30L, config.period)
        assertEquals(HmacAlgorithm.SHA1, config.algorithm)
    }

    @Test
    fun testHotpRejected() {
        val hotpUri = "otpauth://hotp/User?secret=JBSWY3DPEHPK3PXP&counter=1"
        val config = OtpParser.parse(hotpUri)
        assertNull(config)
    }

    @Test
    fun testToOtpAuthUriRoundTrip() {
        val original = OtpConfig(
            secret = "JBSWY3DPEHPK3PXP",
            issuer = "SecureVault",
            account = "user@example.com",
            digits = 6,
            period = 30L,
            algorithm = HmacAlgorithm.SHA1
        )
        val uri = OtpParser.toOtpAuthUri(original)
        assertTrue(uri.startsWith("otpauth://totp/"))
        val parsed = OtpParser.parse(uri)

        assertNotNull(parsed)
        assertEquals(original.secret, parsed!!.secret)
        assertEquals(original.issuer, parsed.issuer)
        assertEquals(original.digits, parsed.digits)
        assertEquals(original.period, parsed.period)
    }

    @Test
    fun testRfc6238StandardVector() {
        // "12345678901234567890" in Base32 is "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"
        // RFC 6238 reference vectors:
        // At Time = 59s: TOTP value is "287082"
        // At Time = 1111111109s: TOTP value is "081804"
        val config = OtpConfig(
            secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ",
            digits = 6,
            period = 30L,
            algorithm = HmacAlgorithm.SHA1
        )

        val fixedClock59 = Clock.fixed(Instant.ofEpochSecond(59L), ZoneOffset.UTC)
        val generator59 = OtpGenerator(config, fixedClock59)
        assertEquals("287082", generator59.generateCode())

        val fixedClock1111111109 = Clock.fixed(Instant.ofEpochSecond(1111111109L), ZoneOffset.UTC)
        val generator111 = OtpGenerator(config, fixedClock1111111109)
        assertEquals("081804", generator111.generateCode())
    }

    @Test
    fun testRemainingSecondsAndProgress() {
        val config = OtpConfig(
            secret = "JBSWY3DPEHPK3PXP",
            digits = 6,
            period = 30L
        )

        // At 10s into the 30s period (e.g. 10_000 ms)
        val clock10 = Clock.fixed(Instant.ofEpochMilli(10_000L), ZoneOffset.UTC)
        val generator = OtpGenerator(config, clock10)

        val remaining = generator.calculateRemainingSeconds()
        assertEquals(20L, remaining)

        val progress = generator.calculateProgress()
        assertEquals(20f / 30f, progress, 0.05f)
    }
}
