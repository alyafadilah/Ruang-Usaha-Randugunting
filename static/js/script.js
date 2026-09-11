document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // MOBILE MENU
    // =====================================================

    const mobileMenuBtn = document.getElementById("mobileMenuBtn");
    const mobileMenu = document.getElementById("mobileMenu");

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener("click", function () {
            mobileMenu.classList.toggle("active");
        });
    }

    // =====================================================
    // SEARCH TABLE
    // =====================================================

    const searchInput = document.getElementById("searchInput");
    const table = document.getElementById("umkmTable");

    if (searchInput && table) {

        searchInput.addEventListener("input", function () {

            const keyword = searchInput.value.toLowerCase().trim();
            const rows = table.querySelectorAll("tbody tr");

            rows.forEach(function (row) {

                const rowText = row.textContent.toLowerCase();

                if (rowText.includes(keyword)) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }

            });

        });

    }

});