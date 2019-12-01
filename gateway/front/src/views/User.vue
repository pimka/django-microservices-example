<template>
    <div>
        <h3>{{ user.username }} information ({{ owner_uuid }})</h3>
        <h2>Properties</h2>
        <PropTable :items="props"/>
        <div class="text-center">
        <b-spinner v-if="props.length == 0" />
        </div>
        <h2>Orders</h2>
        <div class="text-center">
        <b-spinner v-if="orders.length == 0" />
        </div>
        <OrderTable :items="orders"/>
        <b-alert v-for="err in errors" :key="err" show dismissible fade variant="danger">{{ err }}
        </b-alert>
    </div>
</template>

<script>
import { HTTP } from '../api/common'
import PropTable from '../components/Users/PropertiesTable.vue'
import OrderTable from '../components/Users/OrdersTable.vue'

export default {
  components: {
    PropTable,
    OrderTable
  },
  data () {
    return {
      user: {
        type: Object
      },
      owner_uuid: this.$route.params.owner_uuid,
      types: [
        { text: 'Rent', value: 'R' },
        { text: 'Sale', value: 'S' },
        { text: 'Purchase', value: 'P' }
      ],
      props: [],
      orders: [],
      errors: []
    }
  },

  created () {
    this.getData()
  },

  methods: {
    getData () {
      HTTP.get(`/user/${this.owner_uuid}/`).then(response => {
        this.user = response.data
      }).catch(err => { this.errors.push(err.response.statusText) })
      HTTP.get(`/user/${this.owner_uuid}/orders`).then(response => {
        this.orders = response.data
      }).catch(err => {
        this.errors.push(err.response.statusText)
      })
      HTTP.get(`/user/${this.owner_uuid}/props`).then(response => {
        this.props = response.data
      }).catch(err => { this.errors.push(err.response.statusText) })
    }
  }
}
</script>
