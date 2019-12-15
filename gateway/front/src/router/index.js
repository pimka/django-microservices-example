import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Properties from '../views/Properties.vue'
import Orders from '../views/Orders.vue'
import Users from '../views/Users.vue'
import Auth from '../views/Auth.vue'
import Property from '../views/Property.vue'
import Order from '../views/Order.vue'
import User from '../views/User.vue'
import store from '@/store'
import HiddenRedirect from '../views/HiddenRedirect.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/prop/',
    name: 'properties',
    component: Properties
  },
  {
    path: '/prop/:prop_uuid/',
    name: 'concrete_property',
    component: Property,
    meta: {
      Authorization: true
    }
  },
  {
    path: '/order/',
    name: 'orders',
    component: Orders
  },
  {
    path: '/order/:order_uuid/',
    name: 'concrete_order',
    component: Order,
    meta: {
      Authorization: true
    }
  },
  {
    path: '/user/',
    name: 'user',
    component: Users,
    meta: {
      Authorization: true
    }
  },
  {
    path: '/user/:owner_uuid/',
    name: 'concrete_user',
    component: User,
    meta: {
      Authorization: true
    }
  },
  {
    path: '/auth/',
    name: 'auth',
    component: Auth
  },
  {
    path: '/hidden-redirect/',
    name: 'hid_red',
    component: HiddenRedirect
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.Authorization)) {
    console.log(store.getters.isLoggedIn)
    if (store.getters.isLoggedIn) {
      next()
      return
    }
    next('/auth/')
  } else {
    next()
  }
})

export default router
