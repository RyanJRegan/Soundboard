var soundLibrary = JSON.parse(document.getElementById('existing-sounds').innerHTML)
function emptySoundForm() {
  return {
    name: '',
    text: '',
    imageFile: null,
    soundFile: null,
    isUploading: false
  }
}

var app = new Vue({
  el: '#app',
  data: {
    soundboardName: '',
    name: '',
    sounds: [],
    soundLibrary: soundLibrary,
    newSoundForm: emptySoundForm()
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
          this.newSoundForm=emptySoundForm()
          event.target.reset()
          this.$refs.soundImageInput.reset()
          this.$refs.soundSoundInput.reset()
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
    },
    removeSound: function (soundIndex) {
      this.sounds.splice(soundIndex, 1)
    },
    moveSound: function (index, position) {
      var currentSound = this.sounds[index]
      var  targetSound = this.sounds[index + position]
      Vue.set(this.sounds, index + position, currentSound)
      Vue.set(this.sounds, index, targetSound)
    },
    createSoundboard: function (event) {
      event.preventDefault()
      console.log(app.$data.sounds)
      //this.newSoundForm.isUploading = true
      var soundboardFormData = new FormData()
      soundboardFormData.set('soundboardName', app.$data.soundboardName)
      // soundboardFormData.set('sounds', app.$data.sounds)
      soundboardFormData.set('sounds', app.$data.sounds.map(function (sound) {
        return sound.id
      }))
        // if (this.newSoundForm.imageFile !== null) {
        //   formData.set('image_file', this.newSoundForm.imageFile)
        // }

        var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
        var xhr = new XMLHttpRequest()
        xhr.open('POST', '/soundboard/create/', true)
        xhr.setRequestHeader('X-CSRFToken', csrfToken)
        xhr.onload = () => {
          if (xhr.status === 200) {
            var body = JSON.parse(xhr.response)
            location.href = '/soundboard/' + body.id + '/'
            console.log('success')
            //     this.sounds.push(JSON.parse(xhr.response))
            //     this.soundLibrary.push(JSON.parse(xhr.response))
            //     this.newSoundForm=emptySoundForm()
            //     event.target.reset()
            //     this.$refs.soundImageInput.reset()
            //     this.$refs.soundSoundInput.reset()
          } else {
            console.log('An error occurred!');
            //  this.newSoundForm.isUploading = false
          }
        }
        xhr.send(soundboardFormData)
      }}
})


