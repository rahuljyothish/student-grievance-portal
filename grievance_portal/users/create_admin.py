import os
import sys
import django

# Ensure the script can find the Django project
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grievance_portal.settings')
django.setup()

from users.models import User

def create_admin_users():
    admin_data = [
        {'admin_id': 1, 'email': 'hosteladmin@college.com', 'password': 'hostel123', 'admin_role': 'hostel'},
        {'admin_id': 2, 'email': 'infraadmin@college.com', 'password': 'infra123', 'admin_role': 'infra'},
        {'admin_id': 3, 'email': 'examadmin@college.com', 'password': 'exam123', 'admin_role': 'exam'}
    ]

    for data in admin_data:
        if not User.objects.filter(email=data['email'], user_type='admin').exists():
            user = User.objects.create(
                email=data['email'],
                admin_id=data['admin_id'],
                admin_role=data['admin_role'],
                user_type='admin',  # ✅ Make sure to specify it's an admin
                is_staff=True
            )
            user.set_password(data['password'])  # ✅ Hash the password
            user.save()
            print(f"Created admin: {data['email']} with role {data['admin_role']}")
        else:
            print(f"Admin {data['email']} already exists")

if __name__ == "__main__":
    create_admin_users()
    print("Admin users initialization completed!")
