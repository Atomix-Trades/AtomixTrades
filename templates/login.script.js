script.js
// console.log(`jay shree ram`);
let inputs = document.querySelectorAll('input');
let btn = document.querySelector('button');
console.log(btn);
inputs.forEach((element, indexOne) => {
    element.addEventListener('keyup', (e) => {
        let currentElements = element, nextInput = element.nextElementSibling, prevInput = element.previousElementSibling;

        if (currentElements.value.length > 1) {
            currentElements.value = "";
            return;
        }

        if (nextInput && nextInput.hasAttribute('disabled') && currentElements.value !== "") {
            nextInput.removeAttribute('disabled');
            nextInput.focus();
        }

        if (e.key === "Backspace") {
            inputs.forEach((element, indexTwo) => {
                if (indexOne <= indexTwo && prevInput) {
                    element.setAttribute('disabled', true);
                    element.value = "";
                    prevInput.focus();
                }
            })
        }

        if (!inputs[3].disabled && inputs[3].value !== "") {
            btn.classList.add('validate');
            return;
        }

        btn.classList.remove('validate');
    })
})

window.addEventListener('load', () => {
    inputs[0].focus();
})