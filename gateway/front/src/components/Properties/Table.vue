<template>
    <div>
        <b-table v-if="items.length > 0" :fields="fields" :items="items" head-variant="light" table-variant="light" striped="true">
            <template v-slot:cell(prop_uuid)="{ value, item }">
                <router-link :to="{ name: 'concrete_property', params: { prop_uuid: value } }">
                    {{ value }}
                </router-link>
            </template>
            <template v-slot:cell(is_living)="{ value, item }">
                <b-checkbox disabled="true" v-model="value"/>
            </template>
        </b-table>
    </div>
</template>

<script>
export default {
  data () {
    return {
      fields: [
        { key: 'prop_uuid', label: 'UUID' },
        { key: 'addres', label: 'Address' },
        { key: 'area', label: 'Area' },
        { key: 'is_living', label: 'Living' },
        { key: 'owner_uuid', label: 'Owner' }
      ]
    }
  },

  props: {
    items: {
      type: Array
    }
  }
}
</script>
