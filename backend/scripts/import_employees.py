import csv
import os
import sys
import django

# ضبط المسارات حتى يتعرف Django على `backend` و `employees`
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # المسار الرئيسي
sys.path.append(BASE_DIR)  # إضافة المسار الرئيسي إلى PYTHONPATH

# ضبط إعدادات Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "advard.settings")
django.setup()

from employees.models import Employee  # استيراد نموذج الموظفين

# تحديد المسار الصحيح لملف CSV
CSV_FILE_PATH = r"C:\Users\meshal\Desktop\advard_system\employees.csv"

def import_employees():
    with open(CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')  # استخدام الفاصلة المنقوطة كفاصل بيانات
        for row in reader:
            Employee.objects.update_or_create(
                employee_id=row['employee_id'],  # الرقم الوظيفي
                defaults={
                    'name': row['employee_name'],  # الاسم
                    'email': row.get('email', ''),  # الإيميل
                    'phone': row.get('phone_number', ''),  # رقم الجوال
                    'department': row['department'],  # القسم
                    'job_title': row['job_title'],  # الوظيفة
                }
            )
    print("✅ تم استيراد بيانات الموظفين بنجاح!")

if __name__ == "__main__":
    import_employees()
