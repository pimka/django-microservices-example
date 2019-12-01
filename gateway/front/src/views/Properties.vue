<template>
    <div>
      <form>
        <h2>Properties</h2>
        <Table :items="items" v-if="items.length > 0"/>
        <div class="text-center" v-if="items.length == 0">
          <b-spinner/>
        </div>
        <b-alert v-if="err !== ''" show dismissible fade variant="danger">{{ err }}
        </b-alert>
      </form>
      <add v-if="err.length !== ''" :address="address" :area="area" :is_living="is_living" :ownerID="ownerID" :addErr="addErr"/>
    </div>
</template>

<script>
import { HTTP } from '../api/common'
import Table from '../components/Properties/Table.vue'
import Add from '../components/Properties/Add.vue'

export default {
  name: 'properties',
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
      address: '',
      area: 0,
      is_living: false,
      ownerID: '',
      err: ''
    }
  },

  methods: {
    getJSON () {
      HTTP.get('/props/').then(response => {
        this.items = response.data
      }).catch(err => { this.err = err.message })
    }
  }
}
</script>
