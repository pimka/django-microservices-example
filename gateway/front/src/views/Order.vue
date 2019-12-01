<template>
    <div>
        <h3>Edit order: {{ order_uuid }}</h3>
        <b-form v-if="prop !== null">
          <b-form-group id="inputTypeGroup" label="Order Type" label-for="inputType">
            <b-form-select id="inputType" v-model="order.order_type" :options="types"/>
          </b-form-group>
          <b-form-group id="inputCustomerGroup" label="Customer UUID" label-for="inputCustomer">
            <b-form-input id="inputCustomer" v-model="order.customer_uuid" placeholder="Enter customer UUID"/>
          </b-form-group>
          <b-form-group id="inputPropertyGroup" label="Property UUID" label-for="inputProperty">
            <b-form-input id="inputProperty" v-model="order.prop_uuid" placeholder="Enter property UUID"/>
          </b-form-group>
          <b-form-group id="inputPriceGroup" label="Price" label-for="inputPrice">
            <b-form-input id="inputPrice" type="number" v-model="order.price" placeholder="Enter price"/>
          </b-form-group>
          <b-button v-on:click="putData()" variant="primary">PUT</b-button>
          <b-button v-on:click="deleteData()" variant="danger">DELETE</b-button>
        </b-form>
        <div class="text-center" v-else>
          <b-spinner/>
        </div>
        <div class="alert alert-danger" role="alert" v-for="err in errors" :key="err">{{ err }}</div>
    </div>
</template>

<script>
import { HTTP } from '../api/common'

export default {
  data () {
    return {
      order: {
        type: Object
      },
      order_uuid: this.$route.params.order_uuid,
      types: [
        { text: 'Rent', value: 'R' },
        { text: 'Sale', value: 'S' },
        { text: 'Purchase', value: 'P' }
      ],
      errors: []
    }
  },

  created () {
    this.getData()
  },

  methods: {
    getData () {
      HTTP.get(`/orders/${this.order_uuid}/`).then(response => {
        this.order = response.data
      }).catch(err => { this.errors.push(err.message) })
    },
    putData () {
      if (this.validData()) {
        HTTP.put(`/orders/${this.order_uuid}/`, this.order).catch(err => { this.errors.push(err.message) })
      }
    },
    deleteData () {
      HTTP.delete(`/orders/${this.order_uuid}/`).catch(err => { this.err = err.message })
    },
    validData () {
      if (this.order.price <= 0) {
        this.errors.push('Enter correct price')
        return false
      } else {
        return true
      }
    }
  }
}
</script>
