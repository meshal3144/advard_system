function initContractsPage() {
    console.log("📦 بدأ تنفيذ كود العقود");

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    // ✅ تحديث الحالة لكل عقد
    document.querySelectorAll(".contracts-table tbody tr").forEach(row => {
        const endDateStr = row.getAttribute("data-end-date");
        const startDateStr = row.getAttribute("data-start-date");
        const statusCell = row.querySelector(".status-cell");

        try {
            const endDate = new Date(endDateStr);
            const startDate = new Date(startDateStr);

            const daysLeft = Math.ceil((endDate - today) / (1000 * 60 * 60 * 24));

            if (today < startDate) {
                statusCell.innerHTML = '<span class="status-pending">لم يبدأ</span>';
            } else if (daysLeft <= 0) {
                statusCell.innerHTML = '<span class="status-expired">منتهي</span>';
            } else if (daysLeft <= 7) {
                statusCell.innerHTML = '<span class="status-expiring">ينتهي قريبًا</span>';
            } else {
                statusCell.innerHTML = '<span class="status-active">فعال</span>';
            }
        } catch (e) {
            console.error("خطأ في التواريخ", e);
            statusCell.innerHTML = '<span class="status-error">خطأ</span>';
        }
    });

    // ✅ حساب الإحصائيات
    const totalContracts = document.querySelectorAll(".contracts-table tbody tr").length;
    let activeCount = 0, expiringCount = 0, expiredCount = 0;

    document.querySelectorAll(".contracts-table tbody tr").forEach(row => {
        const statusText = row.querySelector(".status-cell").textContent.trim();
        if (statusText.includes("فعال")) activeCount++;
        else if (statusText.includes("قريبًا")) expiringCount++;
        else if (statusText.includes("منتهي")) expiredCount++;
    });

    const summaryContainer = document.querySelector(".contracts-summary") || document.createElement("div");
    summaryContainer.className = "contracts-summary";
    summaryContainer.innerHTML = `
        <span class="badge total-contracts">إجمالي العقود: ${totalContracts}</span>
        <span class="badge active-contracts">العقود الفعالة: ${activeCount}</span>
        <span class="badge expiring-contracts">العقود المنتهية قريبًا: ${expiringCount}</span>
        <span class="badge expired-contracts">العقود المنتهية: ${expiredCount}</span>
    `;
    if (!document.querySelector(".contracts-summary")) {
        document.querySelector(".contracts-table").insertAdjacentElement("beforebegin", summaryContainer);
    }
}

// ✅ تشغيل الدالة لما تجهز الصفحة
document.addEventListener('DOMContentLoaded', function() {
    initContractsPage();
});







// تمرير الروابط من Django إلى جافاسكريبت
const serviceRequestsUrl = "{% url 'service_requests' %}"; // مثل /admin-panel/service-requests/
    
// قائمة بالمسارات المعرفة
// كائن المسارات المحدث (يحتوي على جميع الصفحات)
// كائن المسارات المحدث
const routes = {
    // الصفحات الأساسية
    "dashboard": {name: "لوحة التحكم", path: "dashboard"},
    "profile": {name: "الملف الشخصي", path: "profile"},
    "clients": {name: "العملاء", path: "clients"},
    "companies": {name: "الشركات", path: "companies"},
    "service-requests": {name: "طلبات الخدمات", path: "service-requests"},
    "settings": {name: "الإعدادات", path: "settings"},
    "employees": {name: "إدارة الموظفين", path: "employees"},
    
    // الصفحات الفرعية
    "add_client": {name: "إضافة عميل", path: "add-client"},
    "add_company": {name: "إضافة شركة", path: "companies/add"},
    "edit_company": {name: "تعديل شركة", path: "companies/edit"},
    "company_detail": {name: "تفاصيل الشركة", path: "companies"},
    "client_detail": {name: "تفاصيل العميل", path: "clients"},
    "employee_detail": {name: "بيانات الموظف", path: "employees"},
    "employee_add": {name: "إضافة موظف", path: "employees/add"},
    "employee_edit": {name: "تعديل موظف", path: "employees/edit"},
    "contracts": {name: "العقود", path: "contracts"},
    "add_contract": {name: "إضافة عقد", path: "contracts/add"},
    "contract_detail": {name: "تفاصيل العقد", path: "contracts"}
};

function updateBreadcrumb() {
    const pathParts = window.location.pathname.split('/').filter(Boolean);
    const breadcrumbList = document.getElementById('breadcrumb-list');
    
    // مسح العناصر الحالية (ما عدا الرئيسية)
    while (breadcrumbList.children.length > 1) {
        breadcrumbList.removeChild(breadcrumbList.lastChild);
    }
    
    // بناء المسار حسب الصفحة الحالية
    let currentPath = '/admin-panel/';
    
    // حالة الموظفين
    if (pathParts.includes('employees')) {
        addBreadcrumbItem(currentPath + 'employees/', 'إدارة الموظفين');
        currentPath += 'employees/';
        
        if (pathParts.includes('add')) {
            addBreadcrumbItem(currentPath + 'add/', 'إضافة موظف', false);
        } 
        else if (pathParts.length > 2) {
            const employeeId = pathParts[2];
            addBreadcrumbItem(currentPath + employeeId + '/', 'بيانات الموظف');
            
            if (pathParts.includes('edit')) {
                addBreadcrumbItem(currentPath + employeeId + '/edit/', 'تعديل موظف', false);
            }
            else if (pathParts.includes('delete')) {
                addBreadcrumbItem(currentPath + employeeId + '/delete/', 'حذف موظف', false);
            }
        }
    }
    // حالة الشركات
    else if (pathParts.includes('companies')) {
        addBreadcrumbItem(currentPath + 'companies/', 'الشركات');
        currentPath += 'companies/';
        
        if (pathParts.includes('add')) {
            addBreadcrumbItem(currentPath + 'add/', 'إضافة شركة', false);
        }
        else if (pathParts.length > 2) {
            const companyId = pathParts[2];
            addBreadcrumbItem(currentPath + companyId + '/', 'تفاصيل الشركة');
            
            if (pathParts.includes('edit')) {
                addBreadcrumbItem(currentPath + companyId + '/edit/', 'تعديل شركة', false);
            }
        }
    }
    // حالة العقود
    else if (pathParts.includes('contracts')) {
        addBreadcrumbItem(currentPath + 'contracts/', 'العقود');
        currentPath += 'contracts/';
        
        if (pathParts.includes('add')) {
            addBreadcrumbItem(currentPath + 'add/', 'إضافة عقد', false);
        }
        else if (pathParts.length > 2) {
            const contractId = pathParts[2];
            addBreadcrumbItem(currentPath + contractId + '/', 'تفاصيل العقد', false);
        }
    }
    // يمكن إضافة المزيد من الحالات هنا
}

// دالة مساعدة لإضافة عناصر breadcrumb
function addBreadcrumbItem(url, text, isLink = true) {
    const breadcrumbList = document.getElementById('breadcrumb-list');
    const li = document.createElement('li');
    li.className = 'breadcrumb-item';
    
    if (isLink) {
        li.innerHTML = `<a href="${url}">${text}</a>`;
    } else {
        li.textContent = text;
        li.classList.add('active');
    }
    
    breadcrumbList.appendChild(li);
}

// تحديث breadcrumb عند تحميل الصفحة وتغير المسار
document.addEventListener("DOMContentLoaded", updateBreadcrumb);
window.addEventListener('popstate', updateBreadcrumb);

// تحديث الـ Breadcrumb عند النقر على روابط القائمة الجانبية
document.querySelectorAll('.sidebar-menu a').forEach(link => {
    link.addEventListener('click', function() {
        setTimeout(updateBreadcrumb, 100);
    });
});






// خاص بتقسيم صفحات الجداول 


document.addEventListener("DOMContentLoaded", function () {
    // البحث عن جميع الجداول التي تحتوي على كلاس معين
    const tables = document.querySelectorAll(".data-table");

    tables.forEach(table => {
        // العناصر داخل الجدول
        const tableBody = table.querySelector("tbody");
        const rows = tableBody.querySelectorAll("tr");
        const originalRows = Array.from(rows);
        let filteredRows = originalRows;
        let currentPage = 1;
        let rowsPerPage = parseInt(table.dataset.rowsPerPage || 15); // القيمة الافتراضية من data attribute

        // عناصر الفلترة
        const searchInputs = table.parentElement.querySelectorAll(".filters input");
        const clearFiltersBtn = table.parentElement.querySelector(".filters #clearFilters");

        // عناصر التصفح
        const rowsPerPageSelect = table.parentElement.querySelector("#rowsPerPage");
        const prevPageBtn = table.parentElement.querySelector("#prevPage");
        const nextPageBtn = table.parentElement.querySelector("#nextPage");
        const pageInfo = table.parentElement.querySelector("#pageInfo");

        // دالة عرض الصفوف
        function displayRows() {
            const start = (currentPage - 1) * rowsPerPage;
            const end = start + rowsPerPage;

            rows.forEach(row => row.style.display = "none");
            filteredRows.slice(start, end).forEach((row, index) => {
                row.style.display = "";
                row.cells[0].textContent = start + index + 1;
            });

            const totalPages = Math.ceil(filteredRows.length / rowsPerPage);
            pageInfo.textContent = `صفحة ${currentPage} من ${totalPages}`;
            prevPageBtn.disabled = currentPage === 1;
            nextPageBtn.disabled = currentPage === totalPages;
        }

        // دالة الفلترة
        function filterTable() {
            let hasResults = false;
            const noResultsRow = tableBody.querySelector(".no-results");
            if (noResultsRow) tableBody.removeChild(noResultsRow);

            rows.forEach(row => {
                let matches = true;
                searchInputs.forEach(input => {
                    const value = input.value.trim().toLowerCase();
                    const columnIndex = input.dataset.column; // يجب تحديد العمود في HTML
                    if (value && columnIndex) {
                        const cellText = row.children[columnIndex].textContent.toLowerCase();
                        if (!cellText.includes(value)) matches = false;
                    }
                });

                if (matches) {
                    row.style.display = "";
                    hasResults = true;
                } else {
                    row.style.display = "none";
                }
            });

            if (!hasResults) {
                const noResultsRow = document.createElement("tr");
                noResultsRow.className = "no-results";
                noResultsRow.innerHTML = `<td colspan="${rows[0].cells.length}" class="text-center py-3">لا توجد بيانات مطابقة</td>`;
                tableBody.appendChild(noResultsRow);
            }

            filteredRows = Array.from(rows).filter(row => row.style.display !== "none");
            currentPage = 1;
            displayRows();
        }

        // إعادة تعيين الفلاتر
        function resetFilters() {
            searchInputs.forEach(input => (input.value = ""));
            rows.forEach((row, index) => {
                row.style.display = "";
                row.cells[0].textContent = index + 1;
            });
            filteredRows = originalRows;
            currentPage = 1;
            displayRows();
        }

        // أحداث
        searchInputs.forEach(input => input.addEventListener("input", filterTable));
        if (clearFiltersBtn) clearFiltersBtn.addEventListener("click", resetFilters);
        if (rowsPerPageSelect) {
            rowsPerPageSelect.addEventListener("change", () => {
                rowsPerPage = parseInt(rowsPerPageSelect.value);
                currentPage = 1;
                displayRows();
            });
        }
        if (prevPageBtn) {
            prevPageBtn.addEventListener("click", () => {
                if (currentPage > 1) {
                    currentPage--;
                    displayRows();
                }
            });
        }
        if (nextPageBtn) {
            nextPageBtn.addEventListener("click", () => {
                const totalPages = Math.ceil(filteredRows.length / rowsPerPage);
                if (currentPage < totalPages) {
                    currentPage++;
                    displayRows();
                }
            });
        }

        // التهيئة
        displayRows();
    });
});