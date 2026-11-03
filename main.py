import customtkinter as ctk
from tkinter import messagebox
from crypto_engine import encriptar_mensaje, desencriptar_mensaje

# Configuración de apariencia y tema
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class NoxKeyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NoxKey - Cifrado Privado")
        self.geometry("640x560")
        self.resizable(False, False)

        # Encabezado principal
        self.header_label = ctk.CTkLabel(
            self, 
            text="NoxKey 🔒 Cifrador Privado", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.header_label.pack(pady=(15, 5))

        # Sistema de Pestañas
        self.tabview = ctk.CTkTabview(self, width=600, height=470)
        self.tabview.pack(padx=20, pady=(0, 15), fill="both", expand=True)

        self.tab_cifrar = self.tabview.add("Cifrar Mensaje")
        self.tab_descifrar = self.tabview.add("Descifrar Mensaje")

        # Construcción de la interfaz de cada pestaña
        self._build_tab_cifrar()
        self._build_tab_descifrar()

    def _build_tab_cifrar(self):
        frame = self.tab_cifrar

        # 1. Mensaje original
        lbl_msg = ctk.CTkLabel(frame, text="Mensaje Original:", font=ctk.CTkFont(weight="bold"))
        lbl_msg.pack(anchor="w", padx=10, pady=(10, 2))
        
        self.txt_cifrar_input = ctk.CTkTextbox(frame, height=90, font=ctk.CTkFont(size=13))
        self.txt_cifrar_input.pack(fill="x", padx=10, pady=(0, 8))

        # 2. Clave secreta con opción de mostrar/ocultar
        lbl_key = ctk.CTkLabel(frame, text="Clave Secreta:", font=ctk.CTkFont(weight="bold"))
        lbl_key.pack(anchor="w", padx=10, pady=(2, 2))

        key_subframe = ctk.CTkFrame(frame, fg_color="transparent")
        key_subframe.pack(fill="x", padx=10, pady=(0, 10))

        self.entry_cifrar_key = ctk.CTkEntry(
            key_subframe, 
            show="*", 
            placeholder_text="Ingresa una clave secreta..."
        )
        self.entry_cifrar_key.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.btn_show_cifrar_key = ctk.CTkButton(
            key_subframe, 
            text="👁️", 
            width=40, 
            fg_color="gray30", 
            hover_color="gray40",
            command=lambda: self._toggle_show_key(self.entry_cifrar_key, self.btn_show_cifrar_key)
        )
        self.btn_show_cifrar_key.pack(side="right")

        # 3. Botón Cifrar
        btn_cifrar = ctk.CTkButton(
            frame, 
            text="🔒 Cifrar Mensaje", 
            font=ctk.CTkFont(size=14, weight="bold"),
            height=36,
            command=self._accion_cifrar
        )
        btn_cifrar.pack(fill="x", padx=10, pady=(5, 12))

        # 4. Resultado Cifrado
        lbl_res = ctk.CTkLabel(frame, text="Mensaje Cifrado (Base64):", font=ctk.CTkFont(weight="bold"))
        lbl_res.pack(anchor="w", padx=10, pady=(2, 2))

        self.txt_cifrar_output = ctk.CTkTextbox(frame, height=80, font=ctk.CTkFont(size=12))
        self.txt_cifrar_output.pack(fill="x", padx=10, pady=(0, 8))

        # Barra de acciones inferior (Limpiar y Copiar)
        actions_cifrar = ctk.CTkFrame(frame, fg_color="transparent")
        actions_cifrar.pack(fill="x", padx=10, pady=(0, 10))

        btn_limpiar_cifrar = ctk.CTkButton(
            actions_cifrar,
            text="🗑 Limpiar Texto",
            fg_color="#374151",
            hover_color="#1f2937",
            command=self._limpiar_cifrar
        )
        btn_limpiar_cifrar.pack(side="left")

        self.btn_copy_cifrado = ctk.CTkButton(
            actions_cifrar, 
            text="📋 Copiar al Portapapeles", 
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            command=self._copiar_cifrado
        )
        self.btn_copy_cifrado.pack(side="right")

    def _build_tab_descifrar(self):
        frame = self.tab_descifrar

        # 1. Código Cifrado
        lbl_msg = ctk.CTkLabel(frame, text="Código Cifrado (Base64):", font=ctk.CTkFont(weight="bold"))
        lbl_msg.pack(anchor="w", padx=10, pady=(10, 2))
        
        self.txt_descifrar_input = ctk.CTkTextbox(frame, height=90, font=ctk.CTkFont(size=12))
        self.txt_descifrar_input.pack(fill="x", padx=10, pady=(0, 8))

        # 2. Clave secreta
        lbl_key = ctk.CTkLabel(frame, text="Clave Secreta:", font=ctk.CTkFont(weight="bold"))
        lbl_key.pack(anchor="w", padx=10, pady=(2, 2))

        key_subframe = ctk.CTkFrame(frame, fg_color="transparent")
        key_subframe.pack(fill="x", padx=10, pady=(0, 10))

        self.entry_descifrar_key = ctk.CTkEntry(
            key_subframe, 
            show="*", 
            placeholder_text="Ingresa la clave secreta..."
        )
        self.entry_descifrar_key.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.btn_show_descifrar_key = ctk.CTkButton(
            key_subframe, 
            text="👁️", 
            width=40, 
            fg_color="gray30", 
            hover_color="gray40",
            command=lambda: self._toggle_show_key(self.entry_descifrar_key, self.btn_show_descifrar_key)
        )
        self.btn_show_descifrar_key.pack(side="right")

        # 3. Botón Descifrar
        btn_descifrar = ctk.CTkButton(
            frame, 
            text="🔓 Descifrar Mensaje", 
            font=ctk.CTkFont(size=14, weight="bold"),
            height=36,
            command=self._accion_descifrar
        )
        btn_descifrar.pack(fill="x", padx=10, pady=(5, 12))

        # 4. Resultado Original
        lbl_res = ctk.CTkLabel(frame, text="Mensaje Original Desencriptado:", font=ctk.CTkFont(weight="bold"))
        lbl_res.pack(anchor="w", padx=10, pady=(2, 2))

        self.txt_descifrar_output = ctk.CTkTextbox(frame, height=80, font=ctk.CTkFont(size=13))
        self.txt_descifrar_output.pack(fill="x", padx=10, pady=(0, 8))

        # Barra de acciones inferior (Limpiar y Copiar)
        actions_descifrar = ctk.CTkFrame(frame, fg_color="transparent")
        actions_descifrar.pack(fill="x", padx=10, pady=(0, 10))

        btn_limpiar_descifrar = ctk.CTkButton(
            actions_descifrar,
            text="🗑 Limpiar Texto",
            fg_color="#374151",
            hover_color="#1f2937",
            command=self._limpiar_descifrar
        )
        btn_limpiar_descifrar.pack(side="left")

        self.btn_copy_descifrado = ctk.CTkButton(
            actions_descifrar, 
            text="📋 Copiar Mensaje Original", 
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            command=self._copiar_descifrado
        )
        self.btn_copy_descifrado.pack(side="right")

    def _toggle_show_key(self, entry: ctk.CTkEntry, button: ctk.CTkButton):
        if entry.cget("show") == "*":
            entry.configure(show="")
            button.configure(text="🔒")
        else:
            entry.configure(show="*")
            button.configure(text="👁️")

    def _accion_cifrar(self):
        texto = self.txt_cifrar_input.get("1.0", "end-1c").strip()
        clave = self.entry_cifrar_key.get().strip()

        if not texto:
            messagebox.showwarning("Advertencia", "Por favor ingresa un mensaje para cifrar.")
            return
        if not clave:
            messagebox.showwarning("Advertencia", "Por favor ingresa la clave secreta.")
            return

        try:
            cifrado = encriptar_mensaje(texto, clave)
            self.txt_cifrar_output.delete("1.0", "end")
            self.txt_cifrar_output.insert("1.0", cifrado)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al cifrar: {str(e)}")

    def _accion_descifrar(self):
        cifrado = self.txt_descifrar_input.get("1.0", "end-1c").strip()
        clave = self.entry_descifrar_key.get().strip()

        if not cifrado:
            messagebox.showwarning("Advertencia", "Por favor ingresa el texto cifrado.")
            return
        if not clave:
            messagebox.showwarning("Advertencia", "Por favor ingresa la clave secreta.")
            return

        resultado = desencriptar_mensaje(cifrado, clave)
        self.txt_descifrar_output.delete("1.0", "end")
        self.txt_descifrar_output.insert("1.0", resultado)

        if resultado.startswith("Error"):
            messagebox.showerror("Error de Descifrado", resultado)

    def _limpiar_cifrar(self):
        self.txt_cifrar_input.delete("1.0", "end")
        self.txt_cifrar_output.delete("1.0", "end")
        self.txt_cifrar_input.focus_set()

    def _limpiar_descifrar(self):
        self.txt_descifrar_input.delete("1.0", "end")
        self.txt_descifrar_output.delete("1.0", "end")
        self.txt_descifrar_input.focus_set()

    def _animar_copia(self, boton: ctk.CTkButton, texto_original: str):
        boton.configure(text="¡Copiado!", fg_color="#388e3c", hover_color="#2e7d32")
        self.after(2000, lambda: boton.configure(text=texto_original, fg_color="#2e7d32", hover_color="#1b5e20"))

    def _copiar_cifrado(self):
        contenido = self.txt_cifrar_output.get("1.0", "end-1c").strip()
        if contenido:
            self.clipboard_clear()
            self.clipboard_append(contenido)
            self._animar_copia(self.btn_copy_cifrado, "📋 Copiar al Portapapeles")
        else:
            messagebox.showwarning("Atención", "No hay contenido cifrado para copiar.")

    def _copiar_descifrado(self):
        contenido = self.txt_descifrar_output.get("1.0", "end-1c").strip()
        if contenido and not contenido.startswith("Error"):
            self.clipboard_clear()
            self.clipboard_append(contenido)
            self._animar_copia(self.btn_copy_descifrado, "📋 Copiar Mensaje Original")
        else:
            messagebox.showwarning("Atención", "No hay un mensaje válido para copiar.")


if __name__ == "__main__":
    app = NoxKeyApp()
    app.mainloop()
