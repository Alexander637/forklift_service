document.addEventListener("DOMContentLoaded", function () {
    const tabLinks = document.querySelectorAll(".tab-link");
    const tabContents = document.querySelectorAll(".tab-content");

    function switchTab(tabName) {
        tabContents.forEach(function (content) {
            content.classList.add("hidden");
        });
        tabLinks.forEach(function (link) {
            link.classList.remove("active");
        });

        document.getElementById(tabName).classList.remove("hidden");
        document.querySelector(`[data-tab="${tabName}"]`).classList.add("active");
    }

    tabLinks.forEach(function (link) {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const tabName = this.getAttribute("data-tab");
            switchTab(tabName);
        });
    });

    switchTab("machines");
});