document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-confirm]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const message = form.dataset.confirm || "Are you sure?";
            if (!window.confirm(message)) {
                event.preventDefault();
            }
        });
    });

    document.querySelectorAll("[data-status-form] select").forEach((select) => {
        select.addEventListener("change", () => {
            select.form.requestSubmit();
        });
    });

    window.setTimeout(() => {
        document.querySelectorAll(".alert").forEach((alertElement) => {
            const alert = bootstrap.Alert.getOrCreateInstance(alertElement);
            alert.close();
        });
    }, 4000);
});
