document.addEventListener("DOMContentLoaded", function () {
    // تحديد العناصر الأساسية
    var header = document.getElementById("main-header");
    var logo = document.querySelector(".logo img");
    const navLinks = document.querySelectorAll(".nav a");
    const loginButton = document.querySelector(".btn-primary");

    // التحقق من وجود العناصر قبل المتابعة
if (header && logo) { // إزالة التحقق من logo.complete
    window.addEventListener("scroll", function () {
        if (window.scrollY > 30) {
            header.classList.add("scrolled");
            logo.classList.add("small-logo"); // تطبيق كلاس الحجم الصغير
        } else {
            header.classList.remove("scrolled");
            logo.classList.remove("small-logo"); // إزالة الكلاس عند الرجوع للأعلى
        }
    });

    // تهيئة الحالة عند تحميل الصفحة
    if (window.scrollY > 30) {
        header.classList.add("scrolled");
        logo.classList.add("small-logo");
    } else {
        header.classList.remove("scrolled");
        logo.classList.remove("small-logo");
    }
} else {
    console.log("Error: Header or logo not found.");
}
    // الروابط التفاعلية للتنقل السلس
    if (navLinks.length > 0) {
        navLinks.forEach(link => {
            link.addEventListener("click", function (event) {
                event.preventDefault();
                const targetID = this.getAttribute("href").substring(1);
                const targetElement = document.getElementById(targetID);

                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: "smooth" });
                }
            });
        });
    }

    // تأثيرات على زر تسجيل الدخول
    if (loginButton) {
        loginButton.addEventListener("mouseenter", function () {
            this.classList.add("hover-effect");
        });

        loginButton.addEventListener("mouseleave", function () {
            this.classList.remove("hover-effect");
        });
    }

    // إضافة كود لتفعيل تحديد الرابط النشط
    const activeLinks = document.querySelectorAll(".nav-link");
    if (activeLinks.length > 0) {
        activeLinks.forEach(link => {
            link.addEventListener("click", function () {
                activeLinks.forEach(l => l.classList.remove("active"));
                this.classList.add("active");
            });
        });
    }
});



document.querySelector('.navbar-toggler').addEventListener('click', function() {
    document.querySelector('.navbar-collapse').classList.toggle('show');
});

document.addEventListener('DOMContentLoaded', function () {
    const toggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    if (toggler && navbarCollapse) {
        toggler.addEventListener('click', function () {
            navbarCollapse.classList.toggle('show');
        });
    } else {
        console.error('لم يتم العثور على زر الهامبرغر أو القائمة');
    }
});


    // إظهار القائمة عند التمرير

document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.querySelector(".services-dropdown");
    const megaMenu = dropdown.querySelector(".mega-menu");
    const arrowIcon = dropdown.querySelector(".dropdown-icon");

    // إظهار القائمة عند التمرير
    dropdown.addEventListener("mouseenter", () => {
        megaMenu.style.display = "flex";
        setTimeout(() => {
            megaMenu.style.opacity = "1";
            megaMenu.style.transform = "translateY(0)";
            megaMenu.style.visibility = "visible";
        }, 10); // تأخير بسيط للحركة
    });

    // إخفاء القائمة عند الخروج
    dropdown.addEventListener("mouseleave", () => {
        megaMenu.style.opacity = "0";
        megaMenu.style.transform = "translateY(20px)";
        megaMenu.style.visibility = "hidden";
        setTimeout(() => {
            megaMenu.style.display = "none";
        }, 200); // وقت كافٍ لانتهاء التحول
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const headerLinks = document.querySelectorAll(".header-link"); // استهداف كل الروابط بكلاس header-link

    if (headerLinks.length > 0) {
        headerLinks.forEach(link => {
            link.addEventListener("click", function (e) {
                e.preventDefault(); // منع السلوك الافتراضي

                // استخراج الجزء المطلوب من الـ href (مثلاً attendance-system من attendance-system.html)
                const href = this.getAttribute("href"); // attendance-system.html
                const serviceId = href.split('.')[0]; // attendance-system (إزالة .html)

                // الانتقال للرابط المطلوب
                window.location.href = `/services/${serviceId}/`;
            });
        });
    }
});



document.addEventListener("DOMContentLoaded", function () {
    const serviceBoxes = document.querySelectorAll(".service-box");
    if (serviceBoxes.length > 0) {
        serviceBoxes.forEach((box) => {
            box.addEventListener("click", function () {
                const service = this.getAttribute("data-service");
                window.location.href = `/services/${service}/`;
            });
        });
    }
});


document.addEventListener("DOMContentLoaded", function () {
    // استهداف كل الأرقام في قسم الإحصائيات
    const statNumbers = document.querySelectorAll(".stat-number");

    // إضافة تأثير العد لكل رقم
    statNumbers.forEach(number => {
        const target = parseInt(number.getAttribute("data-target")); // الرقم المستهدف
        let count = 0;
        const increment = target / 100; // سرعة الزيادة (100 خطوة)
        const duration = 2000; // المدة الإجمالية (2 ثانية)
        const intervalTime = duration / 100; // وقت كل خطوة

        const updateNumber = () => {
            count += increment;
            if (count >= target) {
                number.textContent = target; // التوقف عند الرقم المستهدف
                return;
            }
            number.textContent = Math.ceil(count); // تقريب الرقم لأعلى
            setTimeout(updateNumber, intervalTime); // تكرار التحديث
        };

        // تشغيل التأثير عندما يظهر القسم في الشاشة
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateNumber(); // بدء العد عندما يظهر القسم
                    observer.unobserve(entry.target); // إيقاف المراقبة بعد التشغيل
                }
            });
        }, { threshold: 0.5 });

        observer.observe(number);
    });
});


