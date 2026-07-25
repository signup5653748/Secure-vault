import org.linguafranca.pwdb.kdbx.KdbxCredentials
import org.linguafranca.pwdb.kdbx.dom.DomDatabaseWrapper
fun main() {
    val db = DomDatabaseWrapper.create(KdbxCredentials.Password("test".toByteArray()))
    println(db)
}
