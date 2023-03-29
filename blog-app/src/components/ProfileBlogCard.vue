<template>
    <div class="post-card">
        <b-modal :id="blogDetails.blog_id.toString()" title="Delete Post!">
            <p class="my-4">Are you sure you want to delete?</p>
            <div slot="modal-footer" class="w-100">
                <b-button class="float-left" variant="primary"
                    @click="$bvModal.hide(blogDetails.blog_id.toString())">Cancel</b-button>
                <b-button class="float-right" variant="danger" @click="deletePost">Delete</b-button>
            </div>
        </b-modal>

        <b-modal :id="blogDetails.blog_id.toString() + 'update'" title="Edit Post">
            <div>
                <b-form-group id="caption" label="Enter New Caption" label-for="caption-field" valid-feedback="Thank you!">
                    <b-form-input id="caption-field" v-model="caption" trim></b-form-input>
                </b-form-group>
            </div>
            <div slot="modal-footer" class="w-100">
                <b-button class="float-left" variant="primary"
                    @click="$bvModal.hide(blogDetails.blog_id.toString() + 'update')">Cancel</b-button>
                <b-button class="float-right" @click="updateBlogCaption" variant="danger">Update</b-button>
            </div>
        </b-modal>
        <div v-if="isOwner" class="d-flex justify-content-between align-items-center p-2">
            <b-icon-pencil class="h5" @click="$bvModal.show(blogDetails.blog_id.toString() + 'update')"
                style="margin: 0%"></b-icon-pencil>
            <b-icon-trash class="h5" @click="$bvModal.show(blogDetails.blog_id.toString())"
                style="margin: 0%"></b-icon-trash>
        </div>
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
            likeCount: 0,
            isOwner: false,
            caption: this.blogDetails.caption,
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
        },

        async deletePost() {
            await axios.delete(`http://localhost:5000/api/v1/blog/${this.blogDetails.blog_id}`)
                .then(() => {
                    this.$bvToast.toast('Post deleted successfully', {
                        title: 'Success',
                        variant: 'success',
                        solid: true
                    })
                    this.$bvModal.hide(this.blogDetails.blog_id.toString())
                    this.$emit('delete-post', this.blogDetails.blog_id)
                })
                .catch(err => {
                    console.log(err)
                })
        },

        async updateBlogCaption() {
            if (this.caption == this.blogDetails.caption) {
                this.$bvModal.hide(this.blogDetails.blog_id.toString() + 'update')
                return
            }
            let formData = new FormData()
            formData.append('caption', this.caption)
            await axios.put(`http://localhost:5000/api/v1/blog/update-caption/${this.blogDetails.blog_id}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                }
            })
                .then(() => {
                    this.$bvToast.toast('Post caption updated successfully', {
                        title: 'Success',
                        variant: 'success',
                        solid: true
                    })
                    this.$bvModal.hide(this.blogDetails.blog_id.toString() + 'update')
                })
                .catch(err => {
                    console.log(err)
                })
        },

        checkIsOwner() {
            if (this.blogDetails.author_id == this.$store.state.user_id)
                this.isOwner = true
        }
    },
    async created() {
        await this.getLikesCount()
        this.checkIsOwner()
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