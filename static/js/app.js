var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        message: 'vue!'
    },
    methods: {
        onChangeTypeLot(event) {
            console.log("RING RING ");
            console.log(event.target.value)
        }
    }
})