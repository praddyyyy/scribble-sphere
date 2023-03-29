import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import IndexView from '../views/IndexView.vue'
import SignUpView from '../views/SignUpView.vue'
import LikedPostsComponent from '../components/LikedPostsComponent.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'index',
    component: IndexView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUpView
  },
  {
    path: '/dashboard',
    component: HomeView,
    children: [
      {
        path: '',
        component: () => import(/* webpackChunkName: "about" */ '../components/FeedComponent.vue')
      },
      {
        path: 'liked-posts',
        component: LikedPostsComponent
      },
      {
        path: 'people',
        component: () => import(/* webpackChunkName: "about" */ '../components/PeopleComponent.vue')
      }
    ]
  },
  // {
  //   path: '/profile',
  //   name: 'profile',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/ProfileView.vue')
  // },
  {
    path: '/profile/:id',
    name: 'user-profile',
    component: () => import(/* webpackChunkName: "about" */ '../views/ProfileView.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
