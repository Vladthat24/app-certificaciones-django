<script >
import '@fullcalendar/core/vdom' // solves problem with Vite
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'

export default {
  name: 'FormCalendario',
  props: {
  },
  components: {
    FullCalendar,
  },
  data() {
    return {
      tipo: 1,
      dialogState: false,
      currentDay: {},
      calendarOptions: {
        plugins: [
          dayGridPlugin,
          interactionPlugin
        ],
        headerToolbar: {
          // left: 'prev,next, today',
          center: 'title',
          // right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        editable: true,
        selectable: true,
        selectMirror: true,
        dayMaxEvents: true,
        weekends: true,
        select: this.handleDateSelect,
        eventClick: this.handleEventClick,
        locale: 'es',
        events: this.events,
        // initialView: 'dayGridMonth'
        themeSystem: 'cyborg'
      },
    }
  },
  methods: {
    handleEventClick: function (event) {
      this.tipo = 2;
      console.log(" Event");
      this.currentDay = event.event;
      this.dialogState = true;

    },
    handleDateSelect: function (event) {
      this.tipo = 1;
      console.log(" Select ");
      // this.addNewEvent();
      this.currentDay = event;
      this.dialogState = true;

    },
    toggleWeekends: function () {
      this.calendarOptions.weekends = !this.calendarOptions.weekends // toggle the boolean!
    }
    , async addNewEventParent() {
      const rawResponse = await fetch('update', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ date: this.currentDay.startStr })
      });
      const content = await rawResponse.json();

      this.calendarOptions.events = content

      this.dialogState = false;

    }
  }, async created() {
    console.log(" HOla ");
    // GET request using fetch with async/await
    const response = await fetch("list");
    const data = await response.json();
    this.events = data;
    this.calendarOptions.events = data;
    this.calendarOptions.weekends = !this.calendarOptions.weekends
    // this.totalVuePackages = data.total;
  }
}
</script>

<template>

  <button class="btn  btn-dark form-button" @click="toggleWeekends">

    <span v-if="calendarOptions.weekends">Ocultar Fines de semana</span>
    <span v-else>Ver Fines de semana</span>

  </button>
  <FullCalendar :options="calendarOptions" />

  <GDialog v-model="dialogState" max-width="500">
    <div class="modal-dialog modal-lg" role="document">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Confirmar</h5>
      </div>
      <div class="modal-body">
        <div class="form-row">
          <div class="col-md-12">
            <h1 v-if="tipo == 1">
              Agregar día no laborable
            </h1>
            <h1 v-else>
              Quitar día no laborable
            </h1>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-footer">
      <button type="submit" class="btn btn-secondary" @click="dialogState = false">Cancelar</button>
      <button type="button" class="btn btn-primary" @click="addNewEventParent">Aceptar</button>
    </div>
  </GDialog>


</template>

<style lang='css'>
.fc-h-event {
  background-color: #cf0c0c;
  padding: 12% 10%;
  font-size: 12px !important;
}

.fc-toolbar-title {
  font-size: 35px !important;
  color: #046cd3;
  font-weight: 800;
}

.fc-toolbar-chunk:first-child h2 {
  color: #fff !important;
}
</style>