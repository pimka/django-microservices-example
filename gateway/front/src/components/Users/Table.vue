<template>
    <div>
        <b-table v-if="items.length > 0" :fields="fields" :items="items" head-variant="light" table-variant="light" striped="true">
            <template v-slot:cell(owner_uuid)="{ value, item }">
                <router-link :to="{ name: 'concrete_user', params: { owner_uuid: value } }">
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
        { key: 'owner_uuid', label: 'UUID' },
        { key: 'username', label: 'Username' }
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
