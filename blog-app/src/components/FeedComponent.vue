<template>
    <div>
        <div class="new-post-card">
            <div class="new-post-card-text">
                <div>
                    <router-link :to="'/profile/' + userDetails.u_id">
                        <img src="../assets/images/user.png" class="mr-3" width="50px" height="50px" alt="">
                    </router-link>
                </div>
                <p>What's new, {{ userDetails.firstName }}?</p>
            </div>
            <div class="new-post-card-button">
                <b-button v-b-modal.modal-prevent-closing variant="outline-primary" size="sm">Post
                    It!</b-button>
                <b-modal id="modal-prevent-closing" ref="modal" title="Create New Post" @show="resetModal"
                    @hidden="resetModal" @ok="handleOk">
                    <form ref="form" @submit.stop.prevent="handleSubmit">
                        <b-form-group label="Caption" label-for="caption-input" invalid-feedback="Caption is Required"
                            :state="captionState">
                            <b-form-input autocomplete="off" id="caption-input" v-model="caption" :state="captionState"
                                aria-describedby="caption-helper-block" required></b-form-input>
                            <b-form-text id="caption-helper-block">Caption shouldn't exceed a maximum of 50
                                words</b-form-text>

                        </b-form-group>
                        <b-form-group label="Image" label-for="image-input" invalid-feedback="Image is Required"
                            :state="imageState">
                            <b-form-file required accept="image/*" v-model="file" :state="imageState"
                                placeholder="Choose a file or drop it here..." drop-placeholder="Drop file here..."
                                aria-describedby="image-helper-block"></b-form-file>
                            <b-form-text id="image-helper-block">Images must be .jpg, .jpeg, .png or
                                .gif</b-form-text>
                        </b-form-group>
                        <b-button variant="dark" size="sm" class="mt-1" @click="file = null">Clear
                            File</b-button>
                        <div class="mt-3">Selected file: {{ file ? file.name : '' }}</div>
                    </form>
                </b-modal>
            </div>
        </div>
        <div v-for="(blog, index) in blogs" :key="index">
            <post-card :post="blog" :user_id="userDetails.u_id"></post-card>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import PostCardVue from './PostCard.vue';
export default {
    components: {
        PostCard: PostCardVue
    },
    data() {
        return {
            blogs: [],
            userDetails: {},
            caption: '',
            file: null,
            captionState: null,
            imageState: null
        }
    },

    methods: {
        async getUserDetails() {
            await axios.get('http://localhost:5000/api/v1/current-user', {
                headers: { 'x-access-token': localStorage.getItem('token') }
            }).then((res) => {
                this.userDetails = res.data.user
                this.loading = false
            }).catch((err) => {
                console.log(err)
            })
        },
        async getBlogs() {
            await axios.get('http://localhost:5000/api/v1/all-blogs', {
                headers: { 'x-access-token': localStorage.getItem('token') }
            }).then((res) => {
                for (let i = 0; i < res.data.blogs.length; i++) {
                    if (this.following.some(follow => follow.following_id == res.data.blogs[i].author_id)) {
                        this.blogs.push(res.data.blogs[i])
                    }
                }
            }).catch((err) => {
                console.log(err)
            })
        },
        async getFollowing() {
            await axios.get(`http://localhost:5000/api/v1/following/${this.$store.state.user_id}`).then((res) => {
                this.following = res.data.data
            }).catch((err) => {
                console.log(err)
            })
        },
        checkFormValidity() {
            const valid = this.$refs.form.checkValidity()
            this.captionState = valid
            this.imageState = valid
            return valid
        },
        resetModal() {
            this.caption = ''
            this.captionState = null
            this.imageState = null
        },
        handleOk(bvModalEvent) {
            // Prevent modal from closing
            bvModalEvent.preventDefault()
            // Trigger submit handler
            this.handleSubmit()
        },
        async handleSubmit() {
            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return
            }
            var formData = new FormData()
            formData.append('caption', this.caption)
            formData.append('image', this.file)

            // Push the caption to submitted names
            await axios.post('http://localhost:5000/api/v1/blog', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'x-access-token': localStorage.getItem('token')
                }
            }).then(() => {
                this.$bvToast.toast('Post Created Successfully', {
                    title: 'Success',
                    variant: 'success',
                    solid: true
                })
            }).catch(() => {
                this.$bvToast.toast('Something went wrong', {
                    title: 'Error',
                    variant: 'danger',
                    solid: true
                })
            })
            // Hide the modal manually
            this.$nextTick(() => {
                this.$bvModal.hide('modal-prevent-closing')
            })
        },

    },

    async mounted() {
        await this.getUserDetails();
        await this.getFollowing();
        await this.getBlogs();
    },
}
</script>

<style scoped>
.new-post-card {
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
    justify-content: space-between;
}

.new-post-card-text {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}

.new-post-card-text p {
    margin: 0;
    text-align: left;
}
</style>