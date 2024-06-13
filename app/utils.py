from passlib.context import CryptContext
#define password encryption algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



#pip install python-jose[cryptography]     => old way but still works

def hash(password:str):
    return pwd_context.hash(password)


def verify(plain_password, db_password):
    return pwd_context.verify(plain_password, db_password)