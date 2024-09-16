document.addEventListener("DOMContentLoaded", function () {
    const isCustomerCheckbox = document.getElementById("id_is_customer");
    const isEmployeeCheckbox = document.getElementById("id_is_employee");
    const employeeInline = document.getElementById("employee_profile-group");
    const customerInline = document.getElementById("customer_profile-group");

    employeeInline.style.display = "none";
    customerInline.style.display = "none";

    function updateInlineVisibility() {
        if (isCustomerCheckbox.checked && isEmployeeCheckbox.checked) {
            employeeInline.style.display = "block";
            customerInline.style.display = "block";
        } else if (isCustomerCheckbox.checked) {
            employeeInline.style.display = "none";
            customerInline.style.display = "block";
        } else if (isEmployeeCheckbox.checked) {
            customerInline.style.display = "none";
            employeeInline.style.display = "block";
        } else {
            employeeInline.style.display = "none";
            customerInline.style.display = "none";
        }
    }

    isCustomerCheckbox.addEventListener("change", updateInlineVisibility);
    isEmployeeCheckbox.addEventListener("change", updateInlineVisibility);
});
