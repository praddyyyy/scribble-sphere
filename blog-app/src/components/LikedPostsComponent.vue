<template>
    <div>
        <div class="title-card mt-3">
            <h4 class="m-3 ">Your Liked Posts!</h4>
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
            likedBlogs: [],
            blogs: null,
            userDetails: {},
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
        async getLikedBlogs() {
            await axios.get('http://localhost:5000/api/v1/liked-blogs', {
                headers: { 'x-access-token': localStorage.getItem('token') }
            }).then((res) => {
                this.likedBlogs = res.data.data.map(like => like.blog_id)
            }).catch((err) => {
                console.log(err)
            })
        },

        async getBlogs() {
            await axios.get('http://localhost:5000/api/v1/all-blogs', {
                headers: { 'x-access-token': localStorage.getItem('token') }
            }).then((res) => {
                for (let i = 0; i < res.data.blogs.length; i++) {
                    this.blogs = res.data.blogs.filter(blog => this.likedBlogs.includes(blog.blog_id))
                }
            }).catch((err) => {
                console.log(err)
            })
        },
    },
    async mounted() {
        await this.getUserDetails();

        await this.getLikedBlogs()

        await this.getBlogs()
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