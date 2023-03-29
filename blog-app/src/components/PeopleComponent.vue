<template>
    <div>
        <div class="title-card mt-3">
            <h4 class="m-3 ">Connect with people around you!</h4>
        </div>
        <div v-for="(user, index) in users" :key="index">
            <user-card :userDetails="user"></user-card>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import UserCard from './UserCard.vue';
export default {
    components: {
        UserCard
    },
    data() {
        return {
            users: [],
            following: []
        }
    },
    methods: {
        async getAllUsers() {
            await axios.get('http://localhost:5000/api/v1/users', {
                headers: { 'x-access-token': localStorage.getItem('token') }
            }).then((res) => {
                this.users = res.data.users
            }).catch((err) => {
                console.log(err)
            })
        },

        async getFollowing() {
            await axios.get(`http://localhost:5000/api/v1/following/${this.$store.state.user_id}`,).then((res) => {
                this.users = this.users.filter(user => user.u_id != this.$store.state.user_id && !res.data.data.some(following => following.following_id === user.u_id))
            }).catch((err) => {
                console.log(err)
            })
        },
    },
    async mounted() {
        await this.getAllUsers()

        await this.getFollowing()
    }
}
</script>

<style scoped>
.title-card {
    width: 100%;
    border-radius: 10px;
    margin-bottom: 2%;
    margin-top: 1.5%;
    padding: 1%;
    background-color: #fff;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
}
</style>