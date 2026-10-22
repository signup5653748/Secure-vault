package com.example.data

import android.net.Uri
import dev.turingcomplete.kotlinonetimepassword.HmacAlgorithm
import dev.turingcomplete.kotlinonetimepassword.TimeBasedOneTimePasswordConfig
import dev.turingcomplete.kotlinonetimepassword.TimeBasedOneTimePasswordGenerator
import kotlinx.coroutines.currentCoroutineContext
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.isActive
import org.apache.commons.codec.binary.Base32
import java.time.Clock
import java.util.concurrent.TimeUnit

data class OtpConfig(
    val secret: String,
    val issuer: String? = null,
    val account: String? = null,
    val digits: Int = 6,
    val period: Long = 30L,
    val algorithm: HmacAlgorithm = HmacAlgorithm.SHA1
)

data class OtpState(
    val code: String,
    val remainingSeconds: Long,
    val progress: Float,
    val period: Long,
    val formattedCode: String = formatCode(code)
) {
    companion object {
        fun formatCode(code: String): String {
            return if (code.length == 6) {
                "${code.substring(0, 3)} ${code.substring(3)}"
            } else if (code.length == 8) {
                "${code.substring(0, 4)} ${code.substring(4)}"
            } else {
                code
            }
        }
    }
}

object OtpParser {
    private val base32 = Base32()
    private val base32Regex = Regex("^[A-Z2-7]+=*$")

    fun isValidBase32(secret: String): Boolean {
        val clean = cleanSecret(secret)
        if (clean.isEmpty()) return false
        if (!base32Regex.matches(clean)) return false
        return try {
            val decoded = base32.decode(clean)
            decoded != null && decoded.isNotEmpty()
        } catch (_: Exception) {
            false
        }
    }

    fun cleanSecret(secret: String): String {
        return secret.trim()
            .replace(" ", "")
            .replace("-", "")
            .uppercase()
    }

    fun parse(otpValue: String?): OtpConfig? {
        if (otpValue.isNullOrBlank()) return null
        val trimmed = otpValue.trim()

        if (trimmed.startsWith("otpauth://", ignoreCase = true)) {
            return try {
                val questionMarkIdx = trimmed.indexOf('?')
                val queryParams = mutableMapOf<String, String>()
                if (questionMarkIdx != -1) {
                    val queryString = trimmed.substring(questionMarkIdx + 1)
                    queryString.split("&").forEach { pair ->
                        val parts = pair.split("=", limit = 2)
                        if (parts.size == 2) {
                            val k = java.net.URLDecoder.decode(parts[0], "UTF-8").lowercase()
                            val v = java.net.URLDecoder.decode(parts[1], "UTF-8")
                            queryParams[k] = v
                        }
                    }
                }

                val preQuery = if (questionMarkIdx != -1) trimmed.substring(0, questionMarkIdx) else trimmed
                val withoutScheme = preQuery.removePrefix("otpauth://").removePrefix("OTPAUTH://")
                val slashIdx = withoutScheme.indexOf('/')
                val type = if (slashIdx != -1) withoutScheme.substring(0, slashIdx).lowercase() else withoutScheme.lowercase()
                if (type != "totp") {
                    // HOTP or other types are out of scope
                    return null
                }
                val rawPath = if (slashIdx != -1) java.net.URLDecoder.decode(withoutScheme.substring(slashIdx + 1), "UTF-8") else ""

                val secretParam = queryParams["secret"] ?: return null
                val cleanSecret = cleanSecret(secretParam)
                if (!isValidBase32(cleanSecret)) return null

                val digits = queryParams["digits"]?.toIntOrNull()?.coerceIn(6, 8) ?: 6
                val period = queryParams["period"]?.toLongOrNull()?.coerceAtLeast(1L) ?: 30L
                val algoStr = queryParams["algorithm"]?.uppercase() ?: "SHA1"
                val algorithm = when (algoStr) {
                    "SHA256" -> HmacAlgorithm.SHA256
                    "SHA512" -> HmacAlgorithm.SHA512
                    else -> HmacAlgorithm.SHA1
                }
                val issuer = queryParams["issuer"] ?: (if (rawPath.contains(":")) rawPath.substringBefore(":").trim() else null)
                val account = if (rawPath.contains(":")) rawPath.substringAfter(":").trim() else rawPath.trim()

                OtpConfig(
                    secret = cleanSecret,
                    issuer = issuer?.takeIf { it.isNotBlank() },
                    account = account.takeIf { it.isNotBlank() },
                    digits = digits,
                    period = period,
                    algorithm = algorithm
                )
            } catch (_: Exception) {
                null
            }
        } else {
            // Raw Base32 secret fallback
            val cleanSecret = cleanSecret(trimmed)
            if (isValidBase32(cleanSecret)) {
                return OtpConfig(
                    secret = cleanSecret,
                    digits = 6,
                    period = 30L,
                    algorithm = HmacAlgorithm.SHA1
                )
            }
            return null
        }
    }

    fun toOtpAuthUri(config: OtpConfig): String {
        val label = when {
            !config.issuer.isNullOrBlank() && !config.account.isNullOrBlank() ->
                "${config.issuer.trim()}:${config.account.trim()}"
            !config.account.isNullOrBlank() -> config.account.trim()
            !config.issuer.isNullOrBlank() -> config.issuer.trim()
            else -> "Vault"
        }
        val encodedLabel = java.net.URLEncoder.encode(label, "UTF-8").replace("+", "%20")
        val sb = StringBuilder("otpauth://totp/$encodedLabel?secret=${config.secret}")
        sb.append("&digits=${config.digits}")
        sb.append("&period=${config.period}")
        sb.append("&algorithm=${config.algorithm.name}")
        if (!config.issuer.isNullOrBlank()) {
            val encodedIssuer = java.net.URLEncoder.encode(config.issuer.trim(), "UTF-8").replace("+", "%20")
            sb.append("&issuer=$encodedIssuer")
        }
        return sb.toString()
    }
}

class OtpGenerator(
    val config: OtpConfig,
    private val clock: Clock = Clock.systemUTC()
) {
    private val base32 = Base32()
    private val generator: TimeBasedOneTimePasswordGenerator by lazy {
        val secretBytes = base32.decode(config.secret)
        val passwordConfig = TimeBasedOneTimePasswordConfig(
            timeStep = config.period,
            timeStepUnit = TimeUnit.SECONDS,
            codeDigits = config.digits,
            hmacAlgorithm = config.algorithm
        )
        TimeBasedOneTimePasswordGenerator(secretBytes, passwordConfig)
    }

    fun generateCode(timestampMs: Long = clock.millis()): String {
        return try {
            generator.generate(timestampMs)
        } catch (_: Exception) {
            "------"
        }
    }

    fun calculateRemainingSeconds(timestampMs: Long = clock.millis()): Long {
        val periodMs = config.period * 1000L
        val elapsedInPeriod = timestampMs % periodMs
        val remainingMs = periodMs - elapsedInPeriod
        return (remainingMs / 1000L).coerceIn(0L, config.period)
    }

    fun calculateProgress(timestampMs: Long = clock.millis()): Float {
        val periodMs = config.period * 1000L
        val elapsedInPeriod = timestampMs % periodMs
        return (1f - (elapsedInPeriod.toFloat() / periodMs.toFloat())).coerceIn(0f, 1f)
    }

    fun getCurrentState(timestampMs: Long = clock.millis()): OtpState {
        return OtpState(
            code = generateCode(timestampMs),
            remainingSeconds = calculateRemainingSeconds(timestampMs),
            progress = calculateProgress(timestampMs),
            period = config.period
        )
    }

    fun tickerFlow(): Flow<OtpState> = flow {
        var currentSlot: Long = -1L
        var currentCode = ""

        while (currentCoroutineContext().isActive) {
            val nowMs = clock.millis()
            val periodMs = config.period * 1000L
            val slot = nowMs / periodMs

            if (slot != currentSlot || currentCode.isEmpty()) {
                currentSlot = slot
                currentCode = generateCode(nowMs)
            }

            val elapsedInPeriod = nowMs % periodMs
            val remainingMs = periodMs - elapsedInPeriod
            val remainingSec = (remainingMs / 1000L).coerceIn(0L, config.period)
            val progress = (1f - (elapsedInPeriod.toFloat() / periodMs.toFloat())).coerceIn(0f, 1f)

            emit(
                OtpState(
                    code = currentCode,
                    remainingSeconds = remainingSec,
                    progress = progress,
                    period = config.period
                )
            )

            delay(1000L)
        }
    }
}
