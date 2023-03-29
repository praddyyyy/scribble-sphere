<template>
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
            <b-button v-if="!isRequestSent" variant="outline-primary" @click="followUser" size="sm">Follow</b-button>
            <b-button v-if="isRequestSent" variant="outline-primary" @click="deleteFollowRequest" size="sm">Follow Request
                Sent!</b-button>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    props: {
        userDetails: Object
    },
    data() {
        return {
            isRequestSent: false
        }
    },
    methods: {
        async followUser() {
            await axios.post('http://localhost:5000/api/v1/follow', {
                sender_id: this.$store.state.user_id,
                receiver_id: this.userDetails.u_id
            }).then(() => {
                this.isRequestSent = true
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
    },

    async created() {
        await this.checkPendingRequest()
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