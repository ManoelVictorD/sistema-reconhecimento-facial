document.addEventListener('DOMContentLoaded', function() {
    // Atualizar label do file input
    document.querySelectorAll('.inputfile').forEach(input => {
        const label = input.nextElementSibling;
        const labelText = label.querySelector('span');
        
        input.addEventListener('change', function(e) {
            if (this.files.length) {
                labelText.textContent = this.files[0].name;
                label.classList.add('file-selected');
            } else {
                labelText.textContent = 'Selecione um arquivo';
                label.classList.remove('file-selected');
            }
        });
    });

    // Efeito hover nos cards
    document.querySelectorAll('.form-wrapper').forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-2px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });

    // Confirmação para ações críticas
    document.querySelectorAll('form[onsubmit]').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('Tem certeza que deseja realizar esta ação?')) {
                e.preventDefault();
            }
        });
    });

    // Animação de loading para botões
    document.querySelectorAll('.fancy-btn').forEach(btn => {
        const form = btn.closest('form');
        if (btn.type === 'submit' && form) {
            btn.addEventListener('click', function() {
                btn.innerHTML = `
                    <span class="btn-loader"></span>
                    Processando...
                `;
                btn.disabled = true;
            });

            form.addEventListener('submit', function() {
                setTimeout(() => {
                    btn.innerHTML = btn.dataset.originalHtml || btn.innerHTML;
                    btn.disabled = false;
                }, 2000); // Simula um tempo de processamento
            });

            // Salva o HTML original do botão
            btn.dataset.originalHtml = btn.innerHTML;
        }
    });
});