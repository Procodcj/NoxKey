# NoxKey

Aplicación de escritorio para Windows diseñada para el cifrado y descifrado seguro de mensajes de texto. Construida en Python con una interfaz gráfica basada en CustomTkinter y respaldo criptográfico estándar mediante Fernet.

## Características

* **Cifrado simétrico autenticado:** Emplea Fernet (AES-128 en modo CBC con firma HMAC-SHA256 para integridad de datos).
* **Derivación robusta de claves:** Utiliza PBKDF2HMAC con SHA-256 y 480,000 iteraciones para mitigar ataques de fuerza bruta sobre contraseñas.
* **Salt dinámico por mensaje:** Genera un salt criptográfico único de 16 bytes (`os.urandom(16)`) por cada cifrado, prefijado en la carga útil para anular ataques con tablas precalculadas (rainbow tables).
* **Interfaz oscura:** Diseño funcional en modo oscuro con CustomTkinter.

## Requisitos

* Python 3.10 o superior.
* Dependencias principales:
  * `customtkinter`
  * `cryptography`

