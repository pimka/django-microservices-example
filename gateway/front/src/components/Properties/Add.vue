<template>
  <div>
    <h3>Add Property</h3>
    <div class="form-group">
      <label for="addressInput">Address</label>
      <input class="form-control" id="inputAddress" placeholder="Enter address" v-model="address" />
    </div>
    <div class="form-group">
      <label for="inputArea">Area</label>
      <input class="form-control" id="inputArea" placeholder="Enter area" v-model="area" />
    </div>
    <b-form-checkbox-group>
      <b-form-checkbox v-model="is_living">Is Living</b-form-checkbox>
    </b-form-checkbox-group>
    <div class="form-group">
      <label for="inputOwnerID">Owner ID</label>
      <input class="form-control" id="inputOwnerID" placeholder="Enter owner" v-model="ownerID" />
    </div>
    <button type="submit" class="btn btn-primary" v-on:click="sendData()">Submit</button>
    <b-alert v-for="err in addErr" :key="err" show dismissible fade variant="danger">{{ err }}
    </b-alert>
    <b-alert v-if="isSuccess" show dismissible fade variant="success">Success</b-alert>
  </div>
</template>

<script>
import { HTTP } from '../../api/common'

export default {
  props: {
    address: {
      type: String
    },
    area: {
      type: Number
    },
    is_living: {
      type: Boolean
    },
    ownerID: {
      type: String
    },
    addErr: [],
    isSuccess: {
      type: Boolean
    }
  },

  methods: {
    sendData () {
      if (this.validData()) {
        HTTP.post('/props/', {
          'addres': this.address,
          'area': this.area,
          'is_living': this.is_living,
          'owner_uuid': this.ownerID
        }).then(response => {
          this.items = response.data
          this.err = ''
          this.isSuccess = true
        }).catch(err => { this.addErr.push(err.message) })
      }
    },
    validData () {
      this.addErr = []
      if (this.area <= 0) {
        this.addErr.push('Enter correct area')
      }
      if (!this.address) {
        this.addErr.push('Enter correct address')
      }
      if (!this.ownerID) {
        this.addErr.push('Enter correc UUID')
      }
      if (this.addErr.length === 0) {
        return true
      } else {
        return false
      }
    }
  }
}
</script>
