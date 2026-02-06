import bcrypt

class HashManager:
    """
    ALGORİTMA: "Geri Dönüşü Olmayan Mikser" (Hashing)
    ------------------------------------------------
    Özet: Şifreyi bir domatesi ketçap yapmaya benzer şekilde karıştırır. 
          Ketçaba bakarak hangi domatesten yapıldığını anlayamazsınız ama 
          elinizde aynı domates ve tarif varsa aynı sonucu alırsınız.
    
    Amacı: Veritabanı çalınsa bile şifrelerin düz metin olarak görülmesini engellemek.
    """
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Düz metin halindeki şifreyi bcrypt algoritması kullanarak karma hale getirir.
        
        Args:
            password (str): Kullanıcının girdiği düz metin şifre.
            
        Returns:
            str: Veritabanında saklanacak olan güvenli karma şifre.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Girilen şifrenin veritabanındaki karma şifre ile eşleşip eşleşmediğini kontrol eder.
        
        Args:
            password (str): Kontrol edilecek düz metin şifre.
            hashed_password (str): Veritabanında saklanan karma şifre.
            
        Returns:
            bool: Şifreler eşleşiyorsa True, aksi halde False.
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))