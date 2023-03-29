<template>
    <div class="post-card">
        <img :src="getImageSrc(blogDetails.image)" alt="post-image" class="post-image">
        <div class="post-caption">
            <p class="m-0 ml-2">{{ blogDetails.caption }}</p>
        </div>
        <div class="d-flex align-items-center justify-content-between ml-2">
            <div class="d-flex align-items-end">
                <b-icon-heart class="h5" style="margin: 0%"></b-icon-heart>
                <h6 class="m-0 ml-2">{{ likeCount }}</h6>
            </div>
            <div class="d-flex align-items-center">
                <p class="m-0 mr-2"><i><time-ago refresh :datetime="blogDetails.created_at"></time-ago> ago</i></p>
            </div>
        </div>
    </div>
</template>

<script>
import { TimeAgo } from 'vue2-timeago'
import axios from 'axios'
export default {
    props: {
        blogDetails: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            likeCount: 0
        }
    },
    components: {
        TimeAgo
    },
    methods: {
        getImageSrc(imageData) {
            return `data:image/png;base64,${imageData}`
        },

        async getLikesCount() {
            await axios.get(`http://localhost:5000/api/v1/likes-count/${this.blogDetails.blog_id}`)
                .then(res => {
                    this.likeCount = res.data.count
                })
                .catch(err => {
                    console.log(err)
                })
        }
    },
    async mounted() {
        await this.getLikesCount()
    }

}
</script>

<style scoped>
.post-card {
    width: 100%;
    border-radius: 10px;
    margin-bottom: 2%;
    margin-top: 1%;
    padding: 1%;
    background-color: #fff;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
}

.post-image {
    width: 100%;
    height: 15rem;
    margin: 1%;
    border-radius: 10px;
}

.post-caption {
    text-align: left;
    margin-top: 2%;
}
</style>