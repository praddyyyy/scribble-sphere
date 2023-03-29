<template>
    <b-container style="padding-top: 70px">
        <div class="col-12">
            <b-row class="h-100">
                <b-col class="left-container">
                    <router-link class="d-flex mt-3 profile-card" :to="'/profile/' + userDetails.u_id">
                        <div class="user-image">
                            <img src="../assets/images/user.png" width="50px" height="50px" alt="user-image" />
                        </div>
                        <div class="profile-name">
                            <h6 class="m-0"><b>{{ userDetails.firstName + ' ' + userDetails.lastName }}</b></h6>
                            <p class="m-0"><i>@{{ userDetails.username }}</i></p>
                        </div>
                    </router-link>
                    <div class="home-sections">
                        <b-nav vertical class="d-flex flex-column align-items-start w-100">
                            <b-nav-item class="home-nav-item">
                                <router-link :to="{ path: '/dashboard/' }">
                                    <b-icon-newspaper></b-icon-newspaper>
                                    Feed
                                </router-link>
                            </b-nav-item>
                            <b-nav-item class="home-nav-item">
                                <router-link :to="{ path: '/dashboard/people' }">
                                    <b-icon-people></b-icon-people>
                                    People
                                </router-link>
                            </b-nav-item>
                            <b-nav-item class="home-nav-item">
                                <router-link :to="{ path: '/dashboard/liked-posts' }">
                                    <b-icon-bookmark-heart></b-icon-bookmark-heart>
                                    Liked Posts
                                </router-link>
                            </b-nav-item>
                            <b-nav-item class="home-nav-item">
                                <router-link :to="{ path: '/dashboard/bookmarks' }">
                                    <b-icon-bookmark></b-icon-bookmark>
                                    Bookmarks
                                </router-link>
                            </b-nav-item>
                        </b-nav>
                    </div>
                </b-col>
                <b-col class="mid-container" cols="6">
                    <router-view></router-view>
                </b-col>
                <b-col class="right-container">
                    <div>
                        <div>
                            <div class="request-title">
                                <h6>FOLLOW REQUESTS</h6>
                                <div class="request-count">
                                    <p>{{ followRequestCount }}</p>
                                </div>
                            </div>
                            <div style="text-align: left" v-if="followRequestCount == 0">
                                <p><i>You have No Pending Follow Requests</i></p>
                            </div>
                            <div v-for="(user, index) in followRequest" :key="index" class="request-card">
                                <div class="request-card-name">
                                    <img src="../assets/images/user.png" width="50px" height="50px" alt="user-image" />
                                    <p class="request-card-text"><b>{{ user.firstName + ' ' + user.lastName }}</b> wants to
                                        add
                                        you to friends</p>
                                </div>
                                <div class="request-card-buttons">
                                    <b-button variant="outline-primary"
                                        @click="acceptFollowRequest(user.u_id, user.username)" size="sm"
                                        style="width: 45%">Accept</b-button>
                                    <b-button variant="outline-danger" @click="denyFollowRequest(user.u_id, user.username)"
                                        size="sm" style="width: 45%">Decline</b-button>
                                </div>
                            </div>
                        </div>
                    </div>
                </b-col>
            </b-row>
        </div>
    </b-container>
</template>

<script>
import axios from 'axios'
export default {
    props: {
        userDetails: Object
    },
    data() {
        return {
            file: null,
            caption: '',
            captionState: null,
            imageState: null,
            blogs: [],
            followRequestResponse: [],
            followRequestCount: 0,
            followRequest: [],
            following: [],
        }
    },
    methods: {

        async getFollowRequests() {
            await axios.get(`http://localhost:5000/api/v1/follow-requests/${this.$store.state.user_id}`, {
            }).then((res) => {
                this.followRequestResponse = res.data
                this.followRequestCount = res.data.length
                this.followRequestResponse.forEach(async (request) => {
                    await axios.get(`http://localhost:5000/api/v1/user/${request.sender_id}`, {
                        headers: { 'x-access-token': localStorage.getItem('token') }
                    }).then((res) => {
                        this.followRequest.push(res.data.user)
                    }).catch((err) => {
                        console.log(err)
                    })
                })
            }).catch((err) => {
                console.log(err)
            })
        },

        async acceptFollowRequest(sender_id, username) {
            await axios.put(`http://localhost:5000/api/v1/follow-requests/${sender_id}/${this.$store.state.user_id}/accept`, {
            }).then(() => {
                this.$bvToast.toast(`@${username}'s Follow Request Accepted`, {
                    title: 'Success',
                    variant: 'success',
                    solid: true
                })
                this.followRequest = this.followRequest.filter((user) => user.u_id != sender_id)
                this.followRequestCount = this.followRequestCount - 1
            }).catch((err) => {
                console.log(err)
            })
        },

        async denyFollowRequest(sender_id, username) {
            await axios.delete(`http://localhost:5000/api/v1/follow-requests/${sender_id}/${this.$store.state.user_id}/deny`, {
            }).then(() => {
                this.$bvToast.toast(`@${username}'s Follow Request Declined`, {
                    title: 'Success',
                    variant: 'danger',
                    solid: true
                })
                this.followRequest = this.followRequest.filter((user) => user.u_id != sender_id)
                this.followRequestCount = this.followRequestCount - 1
            }).catch((err) => {
                console.log(err)
            })
        }

    },
    async created() {
        await this.getFollowRequests()
    }

}
</script>

<style>
.left-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
}

.mid-container {}

.right-container {}

.profile-card {
    width: 100%;
    padding: 5%;
    border-radius: 10px;
    margin-bottom: 2%;
    margin-top: 2%;
    background-color: #fff;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    text-decoration: none;
    color: #000;
}

.profile-card:hover {
    color: #000;
    text-decoration: none;
}

.profile-card:hover h5 {
    text-decoration: underline;
}

.profile-name {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    margin-left: 5%;
    text-align: left;
}

.home-sections {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 2%;
    margin-top: 5%;
    border-radius: 10px;
    background-color: #fff;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
}

.home-liked-pages {
    margin: 5%;
}

.home-nav-item {
    display: flex;
    flex-direction: row;
    padding: 1%;
    margin: 1% 0 1% 0;
    width: 100%;
}

.home-nav-item:hover {
    background-color: #e6ecf0;
    border-radius: 10px;
}

.right-container h6 {
    margin: 5% 0 5% 0;
    text-align: left;
    font-weight: bold;
}

.request-title {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}

.request-title p {
    margin: 0;
}

.request-count {
    width: 25px;
    height: 25px;
    border-radius: 50%;
    background-color: #1da1f2;
    color: #fff;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
}

.request-card {
    width: 100%;
    padding: 5%;
    border-radius: 10px;
    margin-bottom: 2%;
    margin-top: 2%;
    background-color: #fff;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
}

.request-card-text {
    text-align: left;
    margin: 0;
    margin-left: 5%;
}

.request-card-name {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-left: 5%;
    justify-content: space-between;
}

.request-card-buttons {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-left: 5%;
    margin-top: 5%;
    justify-content: space-between;
}
</style>