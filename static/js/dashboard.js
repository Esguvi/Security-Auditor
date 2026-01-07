document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const targetInput = document.querySelector("input[name='target']");
    const loader = document.getElementById("loader");

    form.addEventListener("submit", (e) => {
        if (!targetInput.value.trim()) {
            e.preventDefault();
            alert("Please enter a valid target");
            return;
        }

        loader.style.display = "block";
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const bars = document.querySelectorAll(".progress-bar");
    bars.forEach(bar => {
        const value = bar.getAttribute("aria-valuenow");
        bar.style.width = "0%";
        setTimeout(() => {
            bar.style.width = value + "%";
        }, 100);
    });
});

const form = document.getElementById("scanForm");
const loader = document.getElementById("loader");

if(form){
    form.addEventListener("submit", () => {
        loader.style.display = "block";
    });
}

function exportPDF() {
    const element = document.getElementById("auditContent");
    if (!element) return;

    html2pdf()
        .from(element)
        .set({
            margin: 10,
            filename: 'security_report.pdf',
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
        })
        .save();
}
