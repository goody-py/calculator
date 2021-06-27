function isInteger(n) {
    return n % 1 === 0;
}

Vue.component('error-object', {
    props: {
        errors: {
            type: Object
        }
    },
    template: `<div>{{errors}}</div>`
});

new Vue({
    el: "#calc",
    component: ['error-object'],
    data: {
        number1: '',
        number2: '',
        result: 'Result',
        error: null
    },
    methods: {
        isInteger,
        validateInputAndGetResult: function () {
            if (!(isInteger(this.number1) && isInteger(this.number2))) {
                this.number1 = isInteger(this.number1) ? this.number1 : ''
                this.number2 = isInteger(this.number2) ? this.number2 : ''
                this.result = 'Input values can only be integers'
            } else {
                this.error = null
                axios.post("/calc", { 
                    number1: parseInt(this.number1), 
                    number2: parseInt(this.number2)
                })
                    .then(resp => resp.data)
                    .then(data => { this.result = data.result })
                    .catch(error => this.error = error.response.data)
            }
        }
    }
})
