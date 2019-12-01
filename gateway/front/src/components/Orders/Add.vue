<template>
    <div>
      <b-form @submit="sendData">
        <h3>Add Order</h3>
        <b-form-group id="inputTypeGroup" label="Order Type" label-for="inputType">
          <b-form-input id="inputType" v-model="type" placeholder="Enter type"/>
        </b-form-group>
        <b-form-group id="inputPropIDGroup" label="Property ID" label-for="inputPropId">
          <b-form-input id="inputPropID" v-model="propID" placeholder="Enter property ID"/>
        </b-form-group>
        <b-form-group id="inputCustIDGroup" label="Customer ID" label-for="inputCustId">
          <b-form-input id="inputCustID" v-model="custID" placeholder="Enter customer ID"/>
        </b-form-group>
        <b-form-group id="inputPriceGroup" label="Property Price" label-for="inputPrice">
          <b-form-input id="inputPrice" v-model="price" placeholder="Enter price"/>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-alert v-for="err in addErr" :key="err" show dismissible fade variant="danger">{{ err }}
        </b-alert>
        <b-alert v-if="isSuccess" show dismissible fade variant="success">Success</b-alert>
      </b-form>
    </div>
</template>

<script>
import { HTTP } from '../../api/common'

export default {
  props: {
    type: {
      type: String
    },
    propID: {
      type: String
    },
    custID: {
      type: String
    },
    price: {
      type: Number
    },
    addErr: [],
    isSuccess: {
      type: Boolean
    }
  },

  methods: {
    sendData () {
      if (this.validData()) {
        HTTP.post('/orders/', {
          'order_type': this.type,
          'customer_uuid': this.custID,
          'price': this.price,
          'prop_uuid': this.propID
        }).then(response => {
          this.items = response.data
          this.err = ''
          this.isSuccess = true
        }).catch(err => { this.addErr.push(err.message) })
      }
    },
    validData () {
      this.addErr = []
      if (this.order.price <= 0) {
        this.addErr.push('Enter correct price')
        return false
      } else {
        return true
      }
    }
  }
}
</script>
