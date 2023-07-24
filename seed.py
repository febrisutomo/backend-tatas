from app import db, app, bcrypt
from models import Role, Gender, BloodType, User
from sqlalchemy import text

def seed_data():
    # Tambahkan data role
    admin_role = Role(name='Admin')
    user_role = Role(name='User')
    db.session.add(admin_role)
    db.session.add(user_role)

    # Tambahkan data gender
    male_gender = Gender(name='Laki-laki')
    female_gender = Gender(name='Perempuan')
    db.session.add(male_gender)
    db.session.add(female_gender)

    # Tambahkan data blood type
    blood_a = BloodType(name='A')
    blood_b = BloodType(name='B')
    blood_ab = BloodType(name='AB')
    blood_o = BloodType(name='O')
    db.session.add(blood_a)
    db.session.add(blood_b)
    db.session.add(blood_ab)
    db.session.add(blood_o)

    db.session.commit()

    # Tambahkan data pengguna
    admin_user = User(name="Admin Febri", email='admin@gmail.com', password=bcrypt.generate_password_hash("admin123").decode('utf-8'), role_id=admin_role.id, gender_id=male_gender.id, blood_type_id=blood_a.id)
    user_user = User(name="User Febri", email='user@gmail.com', password=bcrypt.generate_password_hash("user123").decode('utf-8'), role_id=user_role.id, gender_id=female_gender.id, blood_type_id=blood_b.id)
    db.session.add(admin_user)
    db.session.add(user_user)
    
    # Commit perubahan ke basis data
    db.session.commit()
    
    print("Seeder berhasil dijalankan!")

# Panggil fungsi seeder
if __name__ == '__main__':
    with app.app_context():
        seed_data()

