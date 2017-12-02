var soundLibrary = JSON.parse(document.getElementById('existing-sounds').innerHTML)

var app = new Vue({
  el: '#app',
  data: {
    name: '',
    sounds: [],
    soundLibrary: soundLibrary,
    newSoundForm: {
      name: '',
      text: '',
      imageFile: null,
      soundFile: null,
      isUploading: false
    },
  },
  methods: {
    onNewSoundFormSubmit: function (event) {
      event.preventDefault()
      this.newSoundForm.isUploading = true
      var formData = new FormData()
      formData.set('name', this.newSoundForm.name)
      formData.set('text', this.newSoundForm.text)
      if (this.newSoundForm.imageFile !== null) {
        formData.set('image_file', this.newSoundForm.imageFile)
      }
      formData.set('sound_file', this.newSoundForm.soundFile)

      var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
      var xhr = new XMLHttpRequest()
      xhr.open('POST', '/sounds/create/', true)
      xhr.setRequestHeader('X-CSRFToken', csrfToken)
      xhr.onload = () => {
        if (xhr.status === 200) {
          this.sounds.push(JSON.parse(xhr.response))
          this.soundLibrary.push(JSON.parse(xhr.response))
        } else {
          console.log('An error occurred!');
          this.newSoundForm.isUploading = false
        }
      }
      xhr.send(formData)
    },
    picClick: function (sound) {
      var audio = new Audio(sound.sound_file)
      audio.play()
    },
    addExistingSound: function (sound) {
      this.sounds.push(sound)
    }
  }
})


