<template>
    <div>
      <form>
        <h2>Orders</h2>
        <Table :items="items" v-if="items.length > 0"/>
        <div class="text-center" v-else>
          <b-spinner/>
        </div>
        <div class="alert alert-danger" role="alert" v-if="err !== ''">{{ err }}</div>
        <add :type="type" :propID="propID" :custID="custID" :price="price" :addErr="addErr"/>
      </form>
    </div>
</template>

<script>
import { HTTP } from '../api/common'
import Table from '../components/Orders/Table.vue'
import Add from '../components/Orders/Add.vue'

export default {
  name: 'orders',
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
      type: '',
      propID: '',
      custID: '',
      price: 0,
      err: '',
      addErr: ''
    }
  },

  methods: {
    getJSON () {
      HTTP.get('/orders/').then(response => {
        this.items = response.data
        console.log(response.data)
      }).catch(err => { this.err = err.message })
    }
  }
}
</script>
