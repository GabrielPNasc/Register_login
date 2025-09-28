document.addEventListener('DOMContentLoaded', function() {
    const inputs = document.querySelectorAll('.code-input input');

    inputs.forEach((input, idx) => {
        input.addEventListener('input', function(e) {
            // Só aceita números
            this.value = this.value.replace(/[^0-9]/g, '');
            if (this.value.length === 1 && idx < inputs.length - 1) {
                inputs[idx + 1].focus();
            }
        });

        input.addEventListener('keydown', function(e) {
            if (e.key === 'Backspace' && this.value === '' && idx > 0) {
                inputs[idx - 1].focus();
            }
        });

        input.addEventListener('paste', function(e) {
            const paste = (e.clipboardData || window.clipboardData).getData('text');
            if (/^\d{6}$/.test(paste)) {
                for (let i = 0; i < inputs.length; i++) {
                    inputs[i].value = paste[i];
                }
                inputs[inputs.length - 1].focus();
                e.preventDefault();
            }
        });
    });
});