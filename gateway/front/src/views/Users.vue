<template>
    <div>
        <form class="results">
          <h2>Users</h2>
          <Table :items="items" v-if="items.length > 0"/>
          <div class="text-center" v-else>
            <b-spinner/>
          </div>
          <div class="alert alert-danger" role="alert" v-if="err !== ''">{{ err }}</div>
          <add :username="username" :password="password" :addErr="addErr"/>
        </form>
    </div>
</template>

<script>
import { HTTP } from '../api/common'
import Table from '../components/Users/Table.vue'
import Add from '../components/Users/Add.vue'

export default {
  name: 'users',
  components: {
    Table,
    Add
  },

  created () {
    this.getJSON()
  },

  data () {
    return {
      items: [],
      username: '',
      password: '',
      err: '',
      addErr: ''
    }
  },

  methods: {
    getJSON () {
      HTTP.get('/user/').then(response => {
        this.items = response.data
        console.log(response.data)
      }).catch(err => { this.err = err.message })
    }
  }
}
</script>
