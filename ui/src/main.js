import { createApp,ref } from 'vue'
import App from './App.vue'

// main.js
import 'gitart-vue-dialog/dist/style.css'
import { GDialog } from 'gitart-vue-dialog'
import { plugin as dialogPlugin } from 'gitart-vue-dialog'

const app = createApp({
  // Elemento html donde se va ha renderizar el contenido
  el: '#app',
  // Cambiamos los delimiters de las variables para que sean diferentes a los de Django
  delimiters: ['[[', ']]'],
  // Activamos el componente dentro de la app
  components : {
    App
  },
  // Creamos variable msg reactiva con ref
  data () {
    return {
      msg: ref('xx'),
      tipo: "xx"
    }
  },
})
// Montamos la app en el div #app de nuestra plantilla index.html.
app.component('GDialog', GDialog);
app.use(dialogPlugin).mount("#app");
