// التحكم في قائمة المستخدم من الأيقونة فقط
const dropdownToggle = document.querySelector('.dropdown-toggle');
const dropdownMenu = document.querySelector('.dropdown-menu');

dropdownToggle.addEventListener('click', (e) => {
    e.stopPropagation(); // منع النقر من التأثير على الـ user-info
    dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
});

// إغلاق القائمة عند النقر خارجها
document.addEventListener('click', (e) => {
    if (!dropdownToggle.contains(e.target) && !dropdownMenu.contains(e.target)) {
        dropdownMenu.style.display = 'none';
    }
});



// التحكم في الوضع الليلي
const themeToggle = document.getElementById('theme-toggle');

// عند تحميل الصفحة، تحقق من الحالة المخزنة للوضع الليلي
if (localStorage.getItem('theme') === 'dark') {
    document.body.classList.add('dark-mode'); // تطبيق الوضع الليلي
    themeToggle.classList.replace('ri-moon-line', 'ri-sun-line'); // تغيير الأيقونة
}

// عند النقر على زر التبديل، تشغيل/إيقاف الوضع الليلي
themeToggle.addEventListener('click', () => {
    const isDarkMode = document.body.classList.toggle('dark-mode'); // تبديل الكلاس "dark-mode"
    
    // حفظ الحالة في LocalStorage
    localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');

    // تحديث الأيقونة بناءً على الوضع الحالي
    themeToggle.classList.replace(
        isDarkMode ? 'ri-moon-line' : 'ri-sun-line',
        isDarkMode ? 'ri-sun-line' : 'ri-moon-line'
    );
});


// تمرير الروابط من Django إلى جافاسكريبت
const serviceRequestsUrl = "{% url 'service_requests' %}"; // مثل /admin-panel/service-requests/
    
// قائمة بالمسارات المعرفة
const routes = {
    "dashboard": "لوحة التحكم",
    "profile": "الملف الشخصي",
    "clients": "العملاء",
    "service-requests": "طلبات الخدمات",
    "service_request_detail": "تفاصيل الطلب",
    "settings": "الإعدادات",
    
    "client_detail": "تفاصيل العميل",// إضافة الرابط الجديد هنا
};

// استخراج المسار الاول

let pathParts = window.location.pathname.split("/").filter(Boolean);
let currentPath;

// التعامل مع مسار تفاصيل العميل
if (pathParts.includes("clients") && pathParts.length > 1) {
    currentPath = "client_detail";
} else if (pathParts.includes("service-requests") && pathParts.length > 2) {
    currentPath = "service_request_detail";
} else {
    currentPath = pathParts.pop();
}

let displayText;
const currentPageElement = document.getElementById("current-page");

if (currentPath === "service_request_detail") {
    displayText = '<a href="' + serviceRequestsUrl + '">' + routes["service-requests"] + '</a> / ' + routes["service_request_detail"];
} else if (currentPath === "client_detail") {
    displayText = '<a href="/admin-panel/clients/">' + routes["clients"] + '</a> / ' + routes["client_detail"];
} else {
    displayText = '<a href="/admin-panel/' + currentPath + '/">' + (routes[currentPath] || "صفحة غير معروفة");
}

currentPageElement.innerHTML = displayText;


document.addEventListener("DOMContentLoaded", () => {
    // الحصول على جميع الإشعارات
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach((alert) => {
        // تأخير لمدة 5 ثوانٍ قبل الإخفاء
        setTimeout(() => {
            alert.style.opacity = "0"; // تخفيف الشفافية تدريجيًا
            alert.style.transform = "translateY(-20px)"; // تحريك لأعلى بشكل طفيف

            // إزالة العنصر بالكامل بعد انتهاء التحريك
            setTimeout(() => {
                alert.remove();
            }, 300); // نفس مدة الانتقال في CSS
        }, 5000); // ظهور لمدة 5 ثوانٍ
    });
});




    // جافا سكريبت لفتح وإغلاق المودال بتاع تسجيل الخروج
    function openModal(event) {
        event.preventDefault(); // منع الانتقال الفوري
        document.getElementById("logoutModal").style.display = "block"; // إظهار المودال
    }

    function closeModal() {
        document.getElementById("logoutModal").style.display = "none"; // إخفاء المودال
    }

    function logout() {
        window.location.href = "/logout/"; // توجيه المستخدم إلى صفحة تسجيل الخروج
    }

    // جافا سكريبت لفتح وإغلاق القوائم الجانبية
    document.querySelectorAll('.sidebar-link').forEach(button => {
        button.addEventListener('click', () => {
            const targetMenu = document.getElementById(button.getAttribute('data-target'));
            if (targetMenu) {
                // تحقق إذا القايمة مفتوحة بالفعل
                if (targetMenu.classList.contains('active')) {
                    // إذا مفتوحة، أغلقها
                    targetMenu.classList.remove('active');
                    document.body.classList.remove('sub-sidebar-active');
                    // رجّع العرض للقيمة الأساسية
                    targetMenu.style.width = '200px';
                    document.querySelector('.main-container').style.marginRight = '60px';
                    document.querySelector('.main-container').style.width = 'calc(100% - 60px)';
                    document.querySelector('.panel-header').style.right = '60px';
                    document.querySelector('.panel-footer').style.right = '60px';
                } else {
                    // إذا مش مفتوحة، أغلق كل القوائم التانية وافتح دي
                    document.querySelectorAll('.sub-sidebar').forEach(menu => {
                        menu.classList.remove('active');
                        menu.style.width = '200px'; // رجّع العرض للقيمة الأساسية لكل القوائم
                    });
                    targetMenu.classList.add('active');
                    document.body.classList.add('sub-sidebar-active');
                    // غيّر عرض القايمة الفرعية عشان تملّي المسافة
                    targetMenu.style.width = '220px'; // 200px + 60px (عرض الشريط الرئيسي)
                    // ضبط الحاوية والهيدر والفوتر
                    document.querySelector('.main-container').style.marginRight = '320px'; // 60px + 260px
                    document.querySelector('.main-container').style.width = 'calc(100% - 320px)';
                    document.querySelector('.panel-header').style.right = '320px';
                    document.querySelector('.panel-footer').style.right = '320px';
                }
            }
        });
    });

    // إغلاق القايمة الجانبية لما نضغط خارجها
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.sidebar') && !e.target.closest('.sub-sidebar')) {
            document.querySelectorAll('.sub-sidebar').forEach(menu => {
                menu.classList.remove('active');
                menu.style.width = '200px'; // رجّع العرض للقيمة الأساسية
            });
            document.body.classList.remove('sub-sidebar-active');
            // رجّع العرض للقيمة الأساسية
            document.querySelector('.main-container').style.marginRight = '60px';
            document.querySelector('.main-container').style.width = 'calc(100% - 60px)';
            document.querySelector('.panel-header').style.right = '60px';
            document.querySelector('.panel-footer').style.right = '60px';
        }
    });




   
            // كود تغيير اللغة

    document.getElementById("lang-toggle").addEventListener("click", function () {
        const currentLang = document.documentElement.lang;
        const newLang = currentLang === "ar" ? "en" : "ar";
        document.getElementById("language-input").value = newLang;
        document.getElementById("lang-form").submit();
    });










    
