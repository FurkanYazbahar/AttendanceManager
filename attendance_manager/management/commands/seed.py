from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from api.models import Position, Employee, Department

class Command(BaseCommand):
    help = "Seed initial users and groups"

    def handle(self, *args, **kwargs):
        # Grupları oluştur
        admin_group, created_admin_group = Group.objects.get_or_create(name='admin')
        if created_admin_group:
            self.stdout.write(self.style.SUCCESS("Admin group created"))

        user_group, created_user_group = Group.objects.get_or_create(name='user')
        if created_user_group:
            self.stdout.write(self.style.SUCCESS("User group created"))

        # Admin kullanıcıyı oluştur ve gruba ekle
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                password='admin',
                first_name='admin',
                last_name='admin',
                email='admin@example.com'
            )
            admin_user.groups.add(admin_group)  # Admin grubuna ekle
            self.stdout.write(self.style.SUCCESS("Admin user created and added to Admin group"))

        # Normal kullanıcıyı oluştur ve gruba ekle
        if not User.objects.filter(username='user').exists():
            user = User.objects.create_user(
                username='user',
                password='user',
                first_name='user',
                last_name='user',
                email='user@example.com'
            )
            user.groups.add(user_group)  # User grubuna ekle
            self.stdout.write(self.style.SUCCESS("User created and added to User group"))

        if not Department.objects.filter(name="Technology").exists():
            tech_dept = Department.objects.create(name="Technology", description="The department to which all technical teams are affiliated")
        if not Department.objects.filter(name="Software Development").exists():    
            software_dev_dept = Department.objects.create(name="Software Development", parent_department=tech_dept)


        positions = [
            {"name": "Software Engineer", "description": "General software development tasks."},
            {"name": "Backend Developer", "description": "Responsible for server-side application logic."},
            {"name": "Frontend Developer", "description": "Focuses on user-facing parts of the application."},
            {"name": "DevOps Engineer", "description": "Works on CI/CD and infrastructure automation."},
            {"name": "Data Scientist", "description": "Analyzes and interprets complex data to help companies."},
            {"name": "Product Manager", "description": "Oversees product development and aligns with business goals."},
            {"name": "Quality Assurance Engineer", "description": "Tests and ensures software quality."},
            {"name": "UI/UX Designer", "description": "Designs user-friendly interfaces and experiences."},
            {"name": "Technical Lead", "description": "Leads the technical direction of projects."},
            {"name": "Cybersecurity Analyst", "description": "Focuses on system security and threat analysis."},
        ]

        for position in positions:
            obj, created = Position.objects.get_or_create(name=position['name'], defaults=position)
            if created:
                print(f"Position '{obj.name}' created.")
            else:
                print(f"Position '{obj.name}' already exists.")

        backend_dev = Position.objects.get(name="Backend Developer")
        admin_user = User.objects.get(username='admin')
        software_dev_dept = Department.objects.get(name="Software Development")

        if not Employee.objects.filter(user=admin_user).exists():
            employee1 = Employee.objects.create(
                user=admin_user,
                department=software_dev_dept,
                position=backend_dev,
                hire_date="2023-01-01",
                salary=80000
            )

        frontend_dev = Position.objects.get(name="Frontend Developer")
        user =  User.objects.get(username='user')

        if not Employee.objects.filter(user=user).exists():
            employee2 = Employee.objects.create(
                user=user,
                department=software_dev_dept,
                position=frontend_dev,
                hire_date="2023-02-01",
                manager=employee1  # employee1 çalışanı yöneticisi olarak atanır
            )


        self.stdout.write(self.style.SUCCESS("Seeding completed"))
