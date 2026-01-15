console.log("journal_init.js loaded");

document.addEventListener('DOMContentLoaded', () => {

    function setupFormset({ addBtnId, formsetId, emptyFormId }) {
        const addBtn = document.getElementById(addBtnId);
        const formset = document.getElementById(formsetId);
        const emptyTemplate = document.getElementById(emptyFormId).innerHTML;

        addBtn.addEventListener('click', () => {
            const totalFormsInput =
                formset.closest('.card-body')
                    .querySelector('input[name$="-TOTAL_FORMS"]');

            const index = parseInt(totalFormsInput.value);
            const newFormHtml = emptyTemplate.replace(/__prefix__/g, index);

            formset.insertAdjacentHTML('beforeend', newFormHtml);
            totalFormsInput.value = index + 1;
        });

        formset.addEventListener('click', (e) => {
            if (!e.target.classList.contains('remove-form')) return;

            const form = e.target.closest('.goal-form, .todo-form');
            const deleteInput = form.querySelector('input[type="checkbox"][name$="-DELETE"]');

            if (deleteInput) {
                deleteInput.checked = true;
            }
            form.style.display = 'none';
        });
    }

    setupFormset({
        addBtnId: 'add-goal',
        formsetId: 'goal-formset',
        emptyFormId: 'goal-empty-form'
    });

    setupFormset({
        addBtnId: 'add-todo',
        formsetId: 'todo-formset',
        emptyFormId: 'todo-empty-form'
    });

    // 開始時刻 → 終了時刻制御
    document.addEventListener('change', (e) => {
        if (!e.target.name.endsWith('start_time')) return;

        const form = e.target.closest('.todo-form');
        const endSelect = form.querySelector('select[name$="end_time"]');

        const startValue = e.target.value;
        if (!endSelect.value) {
            endSelect.value = startValue;
        }

        Array.from(endSelect.options).forEach(opt => {
            if (!opt.value) return;
            opt.disabled = opt.value < startValue;
        });
    });
});