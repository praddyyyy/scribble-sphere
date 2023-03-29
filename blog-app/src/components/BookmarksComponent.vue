<template>
    <div>
        <div class="title-card mt-3">
            <h4 class="mt-3 ">Your Saved Posts!</h4>
        </div>

        <div v-if="noSavedPosts" class="mt-5">
            <h2>You have no saved posts!</h2>
        </div>
        <div v-else v-for="(blog, index) in blogs" :key="index">
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
            bookmarkedBlogs: [],
            blogs: null,
            userDetails: {},
            noSavedPosts: false
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

        async getBookmarkedBlogs() {
            await axios.get(`http://localhost:5000/api/v1/bookmarks/${this.userDetails.u_id}`)
                .then((res) => {
                    if (res.data.success === false) {
                        this.noSavedPosts = true
                    } else {
                        this.bookmarkedBlogs = res.data.bookmarks.map(bookmark => bookmark.blog_id)
                        this.noSavedPosts = false
                    }
                }).catch((err) => {
                    console.log(err)
                })
        },

        async getBlogs() {
            await axios.get('http://localhost:5000/api/v1/all-blogs', {
                headers: { 'x-access-token': localStorage.getItem('token') }
            }).then((res) => {
                for (let i = 0; i < res.data.blogs.length; i++) {
                    this.blogs = res.data.blogs.filter(blog => this.bookmarkedBlogs.includes(blog.blog_id))
                }
            }).catch((err) => {
                console.log(err)
            })
        },
    },

    async mounted() {
        await this.getUserDetails()
        await this.getBookmarkedBlogs()
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