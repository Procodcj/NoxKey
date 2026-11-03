import base64
import os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def _generar_fernet(clave_secreta: str, salt: bytes) -> Fernet:
    """Deriva una clave de cifrado Fernet a partir de la contraseña y el salt proporcionados."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480_000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(clave_secreta.encode('utf-8')))
    return Fernet(key)

def encriptar_mensaje(texto_plano: str, clave_secreta: str) -> str:
    """Cifra un mensaje de texto plano usando una clave secreta.
    
    Returns:
        Cadena cifrada en base64 (str).
    """
    if not clave_secreta:
        raise ValueError("La clave secreta no puede estar vacía.")
    
    salt = os.urandom(16)
    fernet = _generar_fernet(clave_secreta, salt)
    fernet_token = fernet.encrypt(texto_plano.encode('utf-8'))
    payload = salt + fernet_token
    return base64.urlsafe_b64encode(payload).decode('utf-8')

def desencriptar_mensaje(texto_cifrado: str, clave_secreta: str) -> str:
    """Desencripta un texto cifrado usando la clave secreta.
    
    Returns:
        Texto plano original desencriptado o mensaje de error.
    """
    if not clave_secreta:
        return "Error: La clave secreta no puede estar vacía."
    
    try:
        datos = base64.urlsafe_b64decode(texto_cifrado.encode('utf-8'))
        if len(datos) < 41:
            return "Error: Clave secreta incorrecta o datos manipulados."
        
        salt = datos[:16]
        fernet_token = datos[16:]
        
        fernet = _generar_fernet(clave_secreta, salt)
        datos_desencriptados = fernet.decrypt(fernet_token)
        return datos_desencriptados.decode('utf-8')
    except InvalidToken:
        return "Error: Clave secreta incorrecta o datos manipulados."
    except Exception as e:
        return f"Error al desencriptar: {str(e)}"

