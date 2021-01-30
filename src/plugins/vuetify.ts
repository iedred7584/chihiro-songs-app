import Vue from "vue"
import Vuetify from "vuetify/lib"

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    themes: {
      light: {
        main: "#7bb3ee",
        sub: "#c4ff9c",
        accent: {
          base: "#f96666",
          lighten1: "#ffd1d1"
        },
        background1: "#f0f8ff",
        background2: "#f0f8ff"
      }
    },
    options: { customProperties: true }
  }
})
