<template>
    <div>
      <b-alert v-for="err in errors" :key="err" show dismissible fade variant="danger">{{ err }}
      </b-alert>
    </div>
</template>

<script>
import { HTTP } from '../api/common'

export default {
  data () {
    return {
      errors: []
    }
  },

  created () {
    this.getToken()
  },

  methods: {
    getToken () {
      HTTP.post('/oauth2/token_exchange/', {
        'code': this.$route.query.code
      }).then(response => {
        this.errors = []
        this.login(response.data)
      }).catch(err => { this.errors.push(err.message) })
    },
    login: function (data) {
      this.$store.dispatch('oauth_login', data)
        .then(() => this.$router.push('/prop/'))
        .catch(error => { this.errors.push(error.response.data.non_field_errors[0]) })
    }
  }
}
</script>
