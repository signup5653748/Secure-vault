repositories {
    mavenCentral()
    maven { url = uri("https://jitpack.io") }
}
configurations.create("testConf")
dependencies {
    "testConf"("com.github.keemobile:kotpass:0.13.0")
}
tasks.register("resolveDependencies") {
    doLast {
        configurations.getByName("testConf").resolve()
        println("Resolved successfully")
    }
}
