document.addEventListener('DOMContentLoaded', () => {
    const cls = 'text-truncate';
    document.querySelectorAll(`.${cls}`).forEach(element => {
        element.addEventListener('click', () => {
            if (element.classList.contains(cls)) {
                element.style.cursor = 'pointer';
                element.classList.remove(cls);
            } else {
                element.classList.add(cls);
            }
        });
    });
});
(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            form.querySelectorAll('input').forEach(input => {
                input.setAttribute('required', '');
            });
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })
})()

// flag that shows whether is shown or not
var toggled = false;

function togglePassword(foo) {
    const input = foo.parentElement.querySelector('input');
    if (!toggled) {
        foo.src = '/static/icons/eye-slash.png';
        toggled = true;
        var type = 'text';
    } else {
        foo.src = '/static/icons/eye.png';
        toggled = false;
        var type = 'password';
    }
    input.type = type;
}

function update_select() {
    const correct = document.querySelector('#correct_choice');
    correct.innerHTML = '<option>Select correct choice</option>';
    document.querySelectorAll('#options input').forEach((input, index) => {
        if (input.value) {
            correct.innerHTML += `<option value="${index}">${input.value}</option>`;
        }
    });
}