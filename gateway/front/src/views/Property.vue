<template>
    <div>
        <h3>Edit property: {{ prop_uuid }}</h3>
        <b-form v-if="prop !== null">
          <b-form-group id="inputAddressGroup" label="Address" label-for="inputAddress">
            <b-form-input id="inputAddress" v-model="prop.addres" placeholder="Enter address"/>
          </b-form-group>
          <b-form-group id="inputAreaGroup" label="Area" label-for="inputArea">
            <b-form-input id="inputArea" type="number" v-model="prop.area" placeholder="Enter area"/>
          </b-form-group>
          <b-form-checkbox-group>
            <b-form-checkbox v-model="prop.is_living">Is Living</b-form-checkbox>
          </b-form-checkbox-group>
          <b-form-group id="inputOwnerGroup" label="Owner UUID" label-for="inputOwner">
            <b-form-input id="inputOwner" v-model="prop.owner_uuid" placeholder="Enter owner UUID"/>
          </b-form-group>
          <b-button v-on:click="putData()" variant="primary">PUT</b-button>
          <b-button v-on:click="deleteData()" variant="danger">DELETE</b-button>
        </b-form>
        <div class="text-center" v-else>
          <b-spinner/>
        </div>
        <b-alert v-for="err in errors" :key="err" show dismissible fade variant="danger">{{ err }}
        </b-alert>
        <b-alert v-if="success != ''" show dismissible fade variant="success">{{ success }}</b-alert>
    </div>
</template>

<script>
import { HTTP } from '../api/common'

export default {
  data () {
    return {
      prop: {
        type: Object
      },
      prop_uuid: this.$route.params.prop_uuid,
      errors: [],
      success: ''
    }
  },

  created () {
    this.getData()
  },

  methods: {
    getData () {
      HTTP.get(`/props/${this.prop_uuid}/`).then(response => {
        this.prop = response.data
      }).catch(err => { this.errors.push(err.response.statusText) })
    },
    putData () {
      if (this.validData()) {
        HTTP.put(`/props/${this.prop_uuid}/`, this.prop).then(response => {
          this.success = 'Property updated'
        }).catch(err => { this.errors.push(err.response.statusText) })
      }
    },
    deleteData () {
      HTTP.delete(`/props/${this.prop_uuid}/`).catch(err => { this.errors.push(err.response.statusText) })
    },
    validData () {
      this.errors = []
      if (this.prop.area <= 0) {
        this.errors.push('Enter correct area')
      }
      if (!this.prop.address) {
        this.errors.push('Enter correct address')
      }
      if (!this.prop.owner_uuid) {
        this.errors.push('Enter correct UUID')
      }
      if (this.errors.length === 0) {
        return true
      } else {
        return false
      }
    }
  }
}
</script>
