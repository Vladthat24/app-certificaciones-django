<template>
<widget-container-modal />
 <FormCalendario v-if="tipo==='calendar'" /> 
</template>

<script>
import FormCalendario from './components/FormCalendario.vue'

export default {
  name: 'App',
  components: {
    FormCalendario,
  },
    props: {
    msg: String,
    tipo: String,
  }
}
</script>
