<template>
    <div>
        <div class="d-flex mt-3 profile-card">
            <router-link :to="'/profile/' + userDetails.u_id" style="width: 50%">
                <div class="d-flex">
                    <div class="user-image">
                        <img src="../assets/images/user.png" width="50px" height="50px" alt="user-image" />
                    </div>
                    <div class="profile-name">
                        <h6 class="m-0"><b>{{ userDetails.firstName + ' ' + userDetails.lastName }}</b></h6>
                        <p class="m-0"><i>@{{ userDetails.username }}</i></p>
                    </div>
                </div>
            </router-link>
            <div>
                <b-button v-if="!isRequestSent && !isFollowing" variant="outline-primary" @click="followUser"
                    size="sm">Follow</b-button>
                <b-button v-if="isRequestSent && !isFollowing" variant="outline-primary" @click="deleteFollowRequest"
                    size="sm">Follow
                    Request
                    Sent!</b-button>
                <b-button v-if="isRemoveButton && follower" variant="outline-danger" size="sm"
                    @click="removeUserFromFollowing" class="mr-2">Remove User</b-button>
                <b-button v-if="isFollowing" variant="outline-primary" @click="unfollowUser" size="sm">Unfollow</b-button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    props: {
        userDetails: Object,
        follower: Boolean
    },
    data() {
        return {
            isRequestSent: false,
            isFollowing: false,
            isRemoveButton: false
        }
    },
    methods: {
        async followUser() {
            await axios.post('http://localhost:5000/api/v1/follow', {
                sender_id: this.$store.state.user_id,
                receiver_id: this.userDetails.u_id
            }).then(() => {
                this.isRequestSent = true
                this.$bvToast.toast(`Follow Request Sent to @${this.userDetails.username}`, {
                    title: 'Success',
                    variant: 'success',
                    solid: true
                })
            }).catch(error => {
                console.log(error)
            })
        },
        async deleteFollowRequest() {
            await axios({
                method: 'delete',
                url: `http://localhost:5000/api/v1/follow-requests/${localStorage.getItem('user_id')}/${this.userDetails.u_id}/deny`,
            }).then((response) => {
                if (response.data.success == true) {
                    this.isRequestSent = false;
                    this.$bvToast.toast(`Follow Request to @${this.userDetails.username} has been Removed!`, {
                        title: 'Success',
                        variant: 'danger',
                        solid: true
                    })
                }
                else {
                    this.$bvToast.toast('Something went wrong', {
                        title: 'Error',
                        variant: 'danger',
                        solid: true
                    })
                }
            }).catch((error) => {
                console.log(error);
            })
        },
        async checkPendingRequest() {
            await axios.get(`http://localhost:5000/api/v1/follow-request-sent/${this.$store.state.user_id}/${this.userDetails.u_id}`,).then((res) => {
                if (res.data.success == true) {
                    this.isRequestSent = true;
                }
            }).catch((err) => {
                console.log(err)
            })
        },

        async checkIfFollowing() {
            await axios.get(`http://localhost:5000/api/v1/is-following/${this.$store.state.user_id}/${this.userDetails.u_id}`,).then((res) => {
                if (res.data.success == true) {
                    this.isFollowing = true;
                }
            }).catch((err) => {
                console.log(err)
            })
        },

        async removeUser() {
            await axios.get(`http://localhost:5000/api/v1/is-following/${this.userDetails.u_id}/${this.$store.state.user_id}`).then((res) => {
                if (res.data.success == true) {
                    this.isRemoveButton = true;
                }
            }).catch((err) => {
                console.log(err)
            })
        },

        async unfollowUser() {
            await axios({
                method: 'delete',
                url: `http://localhost:5000/api/v1/unfollow/${this.$store.state.user_id}/${this.userDetails.u_id}`,
            }).then((response) => {
                if (response.data.success == true) {
                    this.isFollowing = false;
                    this.$bvToast.toast(`Unfollowed @${this.userDetails.username}`, {
                        title: 'Success',
                        variant: 'success',
                        solid: true
                    })
                }
                else {
                    this.$bvToast.toast('Something went wrong', {
                        title: 'Error',
                        variant: 'danger',
                        solid: true
                    })
                }
            }).catch((error) => {
                console.log(error);
            })
        },

        async removeUserFromFollowing() {
            await axios({
                method: 'delete',
                url: `http://localhost:5000/api/v1/remove-follower/${this.userDetails.u_id}/${this.$store.state.user_id}`,
            }).then((response) => {
                if (response.data.success == true) {
                    this.$bvToast.toast(`@${this.userDetails.username} removed from your followers!`, {
                        title: 'Success',
                        variant: 'success',
                        solid: true
                    })
                }
                else {
                    this.$bvToast.toast('Something went wrong', {
                        title: 'Error',
                        variant: 'danger',
                        solid: true
                    })
                }
            }).catch((error) => {
                console.log(error);
            })
        }
    },

    async created() {
        await this.checkPendingRequest()
        await this.checkIfFollowing()
        await this.removeUser()
    },

    watch: {
        userDetails: function () {
            this.checkPendingRequest()
        }
    }
}
</script>

<style scoped>
.profile-card {
    width: 100%;
    padding: 2%;
    border-radius: 10px;
    margin-bottom: 2%;
    margin-top: 2%;
    background-color: #fff;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    text-decoration: none;
    color: #000;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.profile-name {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    margin-left: 2%;
    text-align: left;
    width: 100%;
}
</style>