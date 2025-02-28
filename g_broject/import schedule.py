import schedule
import time as tm
from datetime import datetime

def job(task_time):
    print(f"Task scheduled for {task_time} is running...")
    # هنا يمكنك إضافة أي عمل تريد تنفيذه
    return schedule.CancelJob  # إيقاف المهمة بعد تنفيذها مرة واحدة

# دالة للحصول على التاريخ والوقت من المستخدم
def get_user_input_datetime():
    while True:
        try:
            # طلب تاريخ ووقت من المستخدم
            user_input = input("Enter the date and time for the task (YYYY-MM-DD HH:MM) or type 'exit' to quit: ")
            if user_input.lower() == 'exit':
                return None  # إرجاع None إذا أراد المستخدم إنهاء البرنامج
            # تحليل الإدخال إلى عنصر datetime
            task_datetime = datetime.strptime(user_input, "%Y-%m-%d %H:%M")
            return task_datetime  # إرجاع الوقت كعنصر من نوع datetime
        except ValueError:
            print("Invalid date/time format. Please use YYYY-MM-DD HH:MM (24-hour format).")

# الدالة الرئيسية
if __name__ == "__main__":
    while True:
        # الحصول على التاريخ والوقت من المستخدم
        task_datetime = get_user_input_datetime()

        if task_datetime is None:  # إذا أدخل المستخدم "exit"
            print("Exiting the program. Goodbye!")
            break

        # تحويل الوقت إلى صيغة مناسبة لجدولة المهام
        schedule_date_time = task_datetime.strftime("%Y-%m-%d %H:%M")
        print(f"Task scheduled to run at {schedule_date_time}. Waiting...")

        # حساب الفرق بين الوقت الحالي والوقت المحدد
        current_time = datetime.now()
        time_diff = (task_datetime - current_time).total_seconds()

        if time_diff <= 0:
            print("The specified time has already passed. Please enter a future date and time.")
            continue  # إعادة السؤال إذا كان الوقت قد مر بالفعل

        # جدولة المهمة للتشغيل مرة واحدة
        schedule.every().day.at(task_datetime.strftime("%H:%M")).do(job, task_datetime.strftime("%Y-%m-%d %H:%M"))

        # تشغيل الجدول بشكل مستمر
        while True:
            schedule.run_pending()
            tm.sleep(1)

            # إذا لم تكن هناك أي مهام مجدولة، نخرج من الحلقة الداخلية
            if not schedule.jobs:
                break

        print("Task completed. Do you want to schedule another task?")