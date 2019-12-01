<template>
    <div>
        <form class="add">
          <h3>Add User</h3>
          <div class="form-group">
            <label for="usernameInput">Username</label>
            <input class="form-control" id="inputUsername" placeholder="Enter username" v-model="username"/>
          </div>
          <div class="form-group">
            <label for="inputPassword">Password</label>
            <input class="form-control" id="inputPassword" placeholder="Enter password" v-model="password"/>
          </div>
          <button type="submit" class="btn btn-primary" v-on:click="sendData()">Submit</button>
          <b-alert v-if="addErr.length > 0" show dismissible fade variant="danger">{{ addErr }}
          </b-alert>
          <b-alert v-if="isSuccess" show dismissible fade variant="success">Success</b-alert>
        </form>
    </div>
</template>

<script>
import { HTTP } from '../../api/common'

export default {
  props: {
    username: {
      type: String
    },
    password: {
      type: String
    },
    addErr: {
      type: String
    },
    isSuccess: {
      type: Boolean
    }
  },

  methods: {
    sendData () {
      HTTP.post('/user/', {
        'username': this.username,
        'password': this.password
      }).then(response => {
        this.items = response.data
        this.isSuccess = true
        this.err = ''
      }).catch(err => { this.addErr = err.message })
    }
  }
}
</script>
