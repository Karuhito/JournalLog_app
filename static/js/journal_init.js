console.log("journal.js loaded");

document.addEventListener('DOMContentLoaded', () => {

    // フォームセットの追加/削除
    function setupFormset({ addBtnId, formsetId, emptyFormId, totalFormsId, formClass }) {
        const addBtn = document.getElementById(addBtnId);
        const formset = document.getElementById(formsetId);
        const emptyFormTemplate = document.getElementById(emptyFormId).innerHTML;
        const totalForms = document.getElementById(totalFormsId);

        addBtn.addEventListener('click', () => {
            let formCount = parseInt(totalForms.value);
            let newFormHtml = emptyFormTemplate.replace(/__prefix__/g, formCount);
            formset.insertAdjacentHTML('beforeend', newFormHtml);
            totalForms.value = formCount + 1;
        });

        formset.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-form')) {
                e.target.closest(formClass).remove();
                totalForms.value = parseInt(totalForms.value) - 1;
            }
        });
    }

    setupFormset({
        addBtnId: 'add-goal',
        formsetId: 'goal-formset',
        emptyFormId: 'goal-empty-form',
        totalFormsId: 'id_goal-TOTAL_FORMS',
        formClass: '.goal-form'
    });

    setupFormset({
        addBtnId: 'add-todo',
        formsetId: 'todo-formset',
        emptyFormId: 'todo-empty-form',
        totalFormsId: 'id_todo-TOTAL_FORMS',
        formClass: '.todo-form'
    });

    // 開始時刻と終了時刻の同期 + 終了時刻制限
    function syncEndTimeWithLimit(startSelector, endSelector) {
        document.addEventListener('input', (e) => {
            if (!e.target.matches(startSelector)) return;

            const formGroup = e.target.closest('.todo-form');
            if (!formGroup) return;

            const startValue = e.target.value;
            const endSelect = formGroup.querySelector(endSelector);
            if (!endSelect) return;

            // 終了時刻が空欄なら開始時刻で自動セット
            if (!endSelect.value) {
                endSelect.value = startValue;
            }

            // 終了時刻の選択肢を制限（開始時刻以前は選べない）
            Array.from(endSelect.options).forEach(option => {
                if(option.value === "") return; // 空欄は無効にしない
                option.disabled = option.value < startValue;
            });
        });
    }

    syncEndTimeWithLimit('select[name$="start_time"]', 'select[name$="end_time"]');
});