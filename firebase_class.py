import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import os


load_dotenv()

SDK = os.getenv("SDK")
URL_DB = os.getenv("URL_DB")

class FB:
    def __init__(self):
        
        if not firebase_admin._apps:
            cred = credentials.Certificate(SDK)
            firebase_admin.initialize_app(cred, {
                'databaseURL': URL_DB
            })
        
        
        self.ref = db.reference('server/saving-data')
        self.users_ref = self.ref.child('Users')

    def create(self, animal):
        """
        Recibe un objeto de tipo Animal (Perro, Gato, Pajaro, etc.)
        y lo guarda en la base de datos.
        """
        ref_animal = self.users_ref.child(animal.nombre)

        if ref_animal.get() is None:  
            ref_animal.set({
                'Nombre': animal.nombre,
                'Edad': animal.edad,
                'Tipo': animal.__class__.__name__,
                'Info': animal.info(),
                'Sonido': animal.hablar()
            })
            print(f"✅ Animal '{animal.nombre}' guardado en la nube.")
            return True
        else:
            print(f"⚠️ El animal '{animal.nombre}' ya existe.")
            return False

    def read_all(self):
        """Lee y devuelve todos los animales de la base de datos."""
        data = self.users_ref.get()
        if data:
            return data
        else:
            print("⚠️ No hay datos en la nube.")
            return {}

    def delete(self, nombre):
        """Elimina un animal por su nombre."""
        ref_animal = self.users_ref.child(nombre)
        if ref_animal.get():
            ref_animal.delete()
            print(f"🗑️ Animal '{nombre}' eliminado correctamente.")
        else:
            print(f"⚠️ No se encontró el animal '{nombre}'.")


