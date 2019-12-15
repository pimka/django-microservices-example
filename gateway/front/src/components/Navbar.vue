<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <router-link class="navbar-brand" to='/'>Properties service</router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/prop/">Properties</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/user/">Users</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/order/">Orders</router-link>
          </li>
          <template v-if="!isLoggedIn">
            <li class="nav-item">
              <router-link class="nav-link" to="/auth/">Authorization</router-link>
            </li>
          </template>
          <template v-if="isLoggedIn">
            <li class="nav-item" v-if="isLoggedIn">
              <a class="nav-link" href="#" @click="logout">Logout</a>
            </li>
          </template>
          <template v-if="!isLoggedIn">
            <li class="nav-item">
              <a class="nav-link" href="http://127.0.0.1:8001/o/authorize/?response_type=code&client_id=in7xsewpL5Hisi0ESPGyGz58HQ1eWhc97zObNMVG">OAuth</a>
            </li>
          </template>
        </ul>
      </div>
    </nav>
</template>

<script>
export default {
  computed: {
    isLoggedIn: function () {
      return this.$store.getters.isLoggedIn
    }
  },
  methods: {
    logout: function () {
      this.$store.dispatch('logout')
        .then(() => {
          this.$router.push('/auth/')
        })
    }
  }
}
</script>
