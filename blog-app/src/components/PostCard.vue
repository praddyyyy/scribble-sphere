<template>
    <div class="post-card">
        <div class="post-user">
            <div class="post-user-text">
                <img src="../assets/images/user-1.png" style="border-radius: 50%;" width="50px" height="50px" alt="">
                <div style="text-align: left">
                    <p class="m-0 pl-2"><router-link class="post-author" :to="'/profile/' + post.author_id"><b>@{{
                        post.author }}</b></router-link></p>
                    <p class="m-0 pl-2"><i><time-ago refresh :datetime="post.created_at"></time-ago></i></p>
                </div>
            </div>
            <div v-if="isAuthor()" class="post-user-button">
                <b-dropdown no-caret size="sm" class="m-0 p-0">
                    <template v-slot:button-content>
                        <b-icon-three-dots></b-icon-three-dots>
                    </template>
                    <b-dropdown-item>Edit</b-dropdown-item>
                    <b-dropdown-item>Delete</b-dropdown-item>
                </b-dropdown>
            </div>
        </div>
        <div class="post-caption">
            <p>{{ post.caption }}</p>
        </div>
        <div class="post-image">
            <img :src="getImageSrc(post.image)" width="100%" height="100%" alt="">
        </div>
        <div class="post-buttons">
            <div class="d-flex m-0 ml-1">
                <b-icon-heart v-if="!liked" class="h4" style="margin: 1%" @click="likePost"></b-icon-heart>
                <b-icon-heart-fill variant="danger" v-if="liked" class="h4" style="margin: 1%"
                    @click="dislikePost"></b-icon-heart-fill>
                <p class="m-0 ml-2">{{ likesCount }}</p>
            </div>
            <b-icon-bookmark v-if="!bookmarked" class="h4" style="margin: 1%" @click="bookmarkPost"></b-icon-bookmark>
            <b-icon-bookmark-fill variant="dark" v-if="bookmarked" class="h4" style="margin: 1%"
                @click="unBookmarkPost"></b-icon-bookmark-fill>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { TimeAgo } from 'vue2-timeago'
export default {
    props: {
        post: {
            type: Object,
            required: true
        },
        user_id: {
            type: Number,
            required: true
        }
    },
    data() {
        return {
            liked: false,
            bookmarked: false,
            likesCount: 0
        }
    },
    components: {
        TimeAgo
    },
    methods: {
        getImageSrc(imageData) {
            return `data:image/png;base64,${imageData}`
        },
        isAuthor() {
            if (this.post.author_id === this.user_id) {
                return true
            }
        },
        async likePost() {
            await axios.post('http://localhost:5000/api/v1/like', {
                "user_id": this.user_id,
                "blog_id": this.post.blog_id
            }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
                .then(response => {
                    console.log(response)
                    this.liked = true
                })
                .catch(error => {
                    console.log(error)
                })
        },

        async dislikePost() {
            await axios.put(`http://localhost:5000/api/v1/like/${this.user_id}/${this.post.blog_id}/dislike`)
                .then(() => {
                    this.liked = false
                })
                .catch(error => {
                    console.log(error)
                })
        },

        async getLikes() {
            await axios.get(`http://localhost:5000/api/v1/likes-count/${this.post.blog_id}`)
                .then((response) => {
                    this.likesCount = response.data.count
                })
                .catch(error => {
                    console.log(error)
                })
        },

        async bookmarkPost() {
            await axios.post(`http://localhost:5000/api/v1/bookmark/${this.post.blog_id}/${this.user_id}`)
                .then(() => {
                    this.bookmarked = true
                })
                .catch(error => {
                    console.log(error)
                })
        },

        async unBookmarkPost() {
            await axios.delete(`http://localhost:5000/api/v1/bookmark/${this.post.blog_id}/${this.user_id}/delete`)
                .then(() => {
                    this.bookmarked = false
                })
                .catch(error => {
                    console.log(error)
                })
        },

        async checkIfBookmarked() {
            await axios.get(`http://localhost:5000/api/v1/bookmark/${this.post.blog_id}/${this.user_id}/check`)
                .then((response) => {
                    this.bookmarked = response.data.success
                })
                .catch(error => {
                    console.log(error)
                })
        }

    },
    async mounted() {
        await axios.get(`http://localhost:5000/api/v1/like/${this.user_id}/${this.post.blog_id}/check`)
            .then((response) => {
                this.liked = response.data.success
            })
            .catch(error => {
                console.log(error)
            })

        await this.checkIfBookmarked()

        await this.getLikes()
    },

    watch: {
        liked() {
            if (this.liked) {
                this.likesCount += 1
            } else {
                this.likesCount -= 1
            }
        }
    }
}
</script>

<style>
.post-card {
    width: 100%;
    border-radius: 10px;
    margin-bottom: 2%;
    margin-top: 1%;
    padding: 1%;
    background-color: #fff;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
}

.post-user {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}

.post-user-text {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    padding: 0 1% 0 0;
}

.post-caption {
    text-align: left;
    margin: 1% 0 1% 0;
}

.post-image {
    width: auto;
    height: 30rem;
    margin: 1%;
}

.post-buttons {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}

.post-author {
    text-decoration: none;
    color: #000;
}
</style>