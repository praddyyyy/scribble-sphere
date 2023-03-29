<template>
    <b-container class="profile-container">
        <Navbar :username="currentUser" :user_id="currentUserId" />
        <ProfileHeader :userDetails="userDetails" :isUser="isUser" />
    </b-container>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios'
import ProfileHeader from '../components/ProfileView/ProfileHeader.vue'
import Navbar from '../components/NavBar.vue'
export default {
    components: {
        ProfileHeader,
        Navbar
    },
    data() {
        return {
            isUserAuthenticated: false,
            userDetails: null,
            isUser: false,
            currentUser: null,
            currentUserId: null,
        }
    },
    methods: {
        async getCurrentUser() {
            this.currentUserId = this.$store.state.user_id
            await axios({
                method: 'get',
                url: `http://localhost:5000/api/v1/user/${+this.currentUserId}`,
                headers: { 'x-access-token': localStorage.getItem('token') }
            }).then((res) => {
                this.currentUser = res.data.user.username
            }).catch((err) => {
                console.log(err)
            })
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
            await axios.get(`http://localhost:5000/api/v1/user/${this.$route.params.id}`, {
                headers: { 'x-access-token': localStorage.getItem('token') }
            }).then((res) => {
                this.userDetails = res.data.user
                this.loading = false
                if (res.data.user.u_id === this.$store.state.user_id) {
                    this.isUser = true
                }
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

        await this.getCurrentUser()
    }


}
</script>

<style scoped>
.profile-container {
    height: 100vh;
}
</style>