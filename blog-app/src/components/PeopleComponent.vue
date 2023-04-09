<template>
    <div>
        <div class="title-card mt-3">
            <h4 class="m-3 ">Connect with people around you!</h4>
            <div>
                <b-tabs content-class="mt-3" justified>
                    <b-tab active>
                        <template #title>
                            All ({{ notFollowing.length }})
                        </template>
                        <b-input-group prepend="@">
                            <b-form-input type="search" placeholder="Username" v-model="searchTerm"
                                @input="searchUsers"></b-form-input>
                        </b-input-group>
                        <div v-for="(user, index) in notFollowing" :key="index">
                            <user-card :userDetails="user"></user-card>
                        </div>
                        <h4>SEARCH RESULTS</h4>
                        <div v-for="(user, index) in searchedUsers" :key="index + 1">
                            <user-card :userDetails="user"></user-card>
                        </div>
                    </b-tab>
                    <b-tab>
                        <template #title>
                            Followers ({{ followers.length }})
                        </template>
                        <div v-for="(user, index) in followers" :key="index">
                            <user-card :follower="true" :userDetails="user"></user-card>
                        </div>
                    </b-tab>
                    <b-tab>
                        <template #title>
                            Following ({{ following.length }})
                        </template>
                        <div v-for="(user, index) in following" :key="index">
                            <user-card :userDetails="user"></user-card>
                        </div>
                    </b-tab>
                </b-tabs>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import UserCard from './UserCard.vue';
import LRUCache from 'lru-cache'

export default {
    components: {
        UserCard
    },
    data() {
        return {
            users: [],
            notFollowing: [],
            following: [],
            followers: [],
            searchTerm: '',
            searchedUsers: []
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

        async getNotFollowing() {
            await axios.get(`http://localhost:5000/api/v1/following/${this.$store.state.user_id}`).then((res) => {
                this.notFollowing = this.users.filter(user => user.u_id != this.$store.state.user_id && !res.data.data.some(following => following.following_id === user.u_id))
            }).catch((err) => {
                console.log(err)
            })
        },

        async getFollowing() {
            await axios.get(`http://localhost:5000/api/v1/following/${this.$store.state.user_id}`).then((res) => {
                this.following = this.users.filter(user => user.u_id != this.$store.state.user_id && res.data.data.some(following => following.following_id === user.u_id))
            }).catch((err) => {
                console.log(err)
            })
        },

        async getFollowers() {
            await axios.get(`http://localhost:5000/api/v1/followers/${this.$store.state.user_id}`).then((res) => {
                this.followers = this.users.filter(user => user.u_id != this.$store.state.user_id && res.data.data.some(follower => follower.follower_id === user.u_id))
            }).catch((err) => {
                console.log(err)
            })
        },

        async searchUsers() {
            if (this.searchTerm.length < 1) {
                this.searchedUsers = []
                return
            }

            else {
                if (this.cache.has(this.searchTerm)) {
                    this.searchedUsers = this.cache.get(this.searchTerm)
                    return
                } else {
                    await axios.get(`http://localhost:5000/api/v1/search-user?search=${this.searchTerm}`, {
                        headers: { 'x-access-token': localStorage.getItem('token') }
                    }).then((res) => {
                        this.searchedUsers = res.data.users
                    }).catch((err) => {
                        console.log(err)
                    })
                }
            }
        }
    },
    async created() {
        await this.getAllUsers()

        await this.getNotFollowing()

        await this.getFollowing()

        await this.getFollowers()

        this.cache = new LRUCache({
            max: 100,
        })
    },
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
}
</style>