<template>
    <div>
        <form class="login" @submit.prevent="login">
            <h2>Sign in</h2>
            <div class="form-group">
                <label for="inputUsername">Username</label>
                <input class="form-control" id="inputUsername" placeholder="Enter username" v-model="username"/>
            </div>
            <div class="form-group">
                <label for="inputPassword">Password</label>
                <input type="password" class="form-control" id="inputPassword" placeholder="Enter password" v-model="password"/>
            </div>
            <button type="submit" class="btn btn-primary" v-on:click="login()">Submit</button>
            <div class="alert alert-danger" role="alert" v-if="err !== ''">{{ err }}</div>
            <div class="alert alert-success" role="alert" v-if="is_success">Success</div>
        </form>
    </div>
</template>

<script>
export default {
  name: 'auth',

  data () {
    return {
      username: null,
      password: null,
      err: '',
      is_success: false
    }
  },

  methods: {
    login: function () {
      let username = this.username
      let password = this.password
      this.$store.dispatch('login', { username, password })
        .then(() => this.$router.push('/prop/'))
        .catch(error => { this.err = error.response.data.non_field_errors[0] })
    }
  }
}
</script>
