<template>
  <div class="home">
    <Navbar :username="userDetails.username" :user_id="userDetails.u_id" />
    <div v-if="loading">
      <h1 style="margin-top:150px">Loading...</h1>
    </div>
    <HomeContainer v-else :userDetails="userDetails" />
  </div>
</template>

<script>
import HomeContainer from '../components/HomeContainer.vue'
import Navbar from '../components/NavBar.vue'
import axios from 'axios'
import { mapGetters } from 'vuex'
// @ is an alias to /src
export default {
  name: 'HomeView',
  components: {
    HomeContainer,
    Navbar
  },
  data() {
    return {
      userDetails: {},
      isUserAuthenticated: false,
      loading: true
    }
  },
  computed: {
    ...mapGetters({
      isAuthenticated: 'IS_AUTHENTICATED',
    })
  },
  async mounted() {
    if (this.isAuthenticated) {
      this.isUserAuthenticated = true
      await axios.get('http://localhost:5000/api/v1/current-user', {
        headers: { 'x-access-token': localStorage.getItem('token') }
      }).then((res) => {
        this.userDetails = res.data.user
        this.loading = false
      }).catch((err) => {
        console.log(err)
      })
    } else {

      setTimeout(() => {
        this.$bvToast.toast('Please login to continue', {
          title: 'Login Required',
          variant: 'danger',
          solid: true
        })
      }, 1000)
      this.$router.push('/')
    }

  },
}
</script>
