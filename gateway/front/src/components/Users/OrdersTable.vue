<template>
    <div>
        <b-table v-if="items.length > 0" :fields="fields" :items="items" head-variant="light" table-variant="light" striped="true">
            <template v-slot:cell(order_uuid)="{ value, item }">
                <router-link :to="{ name: 'concrete_order', params: { order_uuid: value } }">
                    {{ value }}
                </router-link>
            </template>
        </b-table>
    </div>
</template>

<script>
export default {
  data () {
    return {
      fields: [
        { key: 'order_uuid', label: 'UUID' },
        { key: 'order_type', label: 'Type' },
        { key: 'prop_uuid', label: 'Property' },
        { key: 'price', label: 'Price' }
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
