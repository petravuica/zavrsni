document.addEventListener('DOMContentLoaded', function () {
    var inputs = document.querySelectorAll('.form-floating .form-control');

    function checkInput(event) {
        var input = event.target;
        var label = input.nextElementSibling;
        if (input.value.trim() !== '' || document.activeElement === input) {
            label.classList.add('float');
        } else {
            label.classList.remove('float');
        }
    }

    inputs.forEach(function(input) {
        input.addEventListener('focus', checkInput);
        input.addEventListener('blur', checkInput);
        input.addEventListener('input', checkInput);
        // Initial check to see if any field should have the floating label applied
        checkInput({ target: input });
    });
});
 