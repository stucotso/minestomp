import com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar

plugins {
    id("java")
    id("com.github.johnrengelman.shadow") version "7.1.0"
}

tasks {
    jar {
        archiveFileName.set("launcher.jar")
    }
}

version = "0.1"

repositories {
    mavenCentral()
    maven(url = "https://jitpack.io")
}

dependencies {
    implementation("com.github.Minestom:Minestom:f80f653ee0")
    implementation(libs.jNoise)
    implementation(files("libs/jython-standalone-2.7.2.jar"))
}

tasks.withType<JavaCompile> {
    options.encoding = "UTF-8"
}

tasks.getByName<Test>("test") {
    useJUnitPlatform()
}

tasks {
    named<ShadowJar>("shadowJar") {
        manifest {
            attributes (
                "Main-Class" to "launcher.Minestomp",
                "Multi-Release" to true
            )
        }
        archiveBaseName.set("minestomp")
        mergeServiceFiles()
    }

    build { dependsOn(shadowJar) }
}