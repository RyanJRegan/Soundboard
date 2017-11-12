var app = new Vue({
  el: '#app',
  data: {
    name: '',
    sounds: [],
    newSoundForm: {
      name: '',
      text: '',
      imageFile: null,
      soundFile: null
    },
  },
  methods: {
    onNewSoundFormSubmit: function (event) {
      event.preventDefault()
      console.log('submitted the form!')
    }
  }
})


