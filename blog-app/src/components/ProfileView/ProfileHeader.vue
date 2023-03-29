<template>
    <div class="header-card">
        <div class="profile-cover">
            <img src="../../assets/images/profile-cover.jpg" height="100%" width="100%" alt="profile-cover">
            <img src="../../assets/images/user.png" height="175px" width="175px" alt="profile-pic" class="profile-image">
        </div>
        <div class="profile-details d-flex align-items-center justify-content-between">
            <div>
                <div v-if="userDetails !== null" class="profile-name">
                    <h3>{{ userDetails.firstName + ' ' + userDetails.lastName }}</h3>
                </div>
                <div v-if="userDetails !== null" class="profile-bio">
                    <p>{{ userDetails.bio }}</p>
                </div>
            </div>
            <div v-if="isFollowing" style="margin-right: 10%">
                <b-button @click="unfollowUser" variant="outline-primary">Unfollow</b-button>
            </div>
            <div v-else style="margin-right: 10%">
                <div v-if="!isCurrentUser && (userDetails !== null)">
                    <div v-if="!isRequestSent">
                        <b-button @click="sendFollowRequest" variant="outline-primary">Follow</b-button>
                    </div>

                    <div v-else class="profile-follow-button">
                        <b-button @click="deleteFollowRequest" variant="outline-primary">Request Sent!</b-button>
                    </div>
                </div>
            </div>
        </div>
        <div class="tabs-container">
            <b-tabs pills card fill content-class="mt-3">
                <b-tab active>
                    <template v-slot:title>
                        <b-icon-person-circle class="mr-2"></b-icon-person-circle>
                        <span>About</span>
                    </template>
                    <div v-if="isProfileVisible">
                        <div class="d-flex align-items-center justify-content-center">
                            <div class="mr-3">
                                <b-icon-lock class="mr-2"></b-icon-lock>
                                <span>PRIVATE ACCOUNT</span>
                            </div>
                        </div>
                    </div>
                    <div v-else>
                        <div v-if="!isCurrentUser">
                            <p v-if="!loading && userProfile.description != null" style="text-align: left">{{
                                userProfile.description }}<span v-if="isCurrentUser" class="ml-2"><b-icon-pen-fill
                                        @click="$bvModal.show('bv-modal-description')"></b-icon-pen-fill></span></p>
                            <div v-if="!loading && userProfile.current_location != null" class="about-card">
                                <b-icon-geo-alt-fill class="mr-2"></b-icon-geo-alt-fill>
                                <div class="location-text">
                                    <p>Lives in <b>{{ userProfile.current_location }}</b></p>
                                </div>
                            </div>

                            <div v-if="!loading && userProfile.profession != null" class="about-card">
                                <b-icon-briefcase class="mr-2"></b-icon-briefcase>
                                <div class="location-text">
                                    <p>{{ userProfile.profession }} at <b>{{ userProfile.current_company }}</b></p>
                                </div>
                            </div>

                            <div v-if="!loading && userProfile.primary_link != null" class="about-card">
                                <b-icon-person class="mr-2"></b-icon-person>
                                <div class="location-text">
                                    <p><b>{{ userProfile.primary_link }}</b></p>
                                </div>
                            </div>

                            <div
                                v-if="!loading && userProfile.current_location == null && userProfile.current_company == null && userProfile.description == null && userProfile.profession == null && userProfile.primary_link == null">
                                <h2>User Profile hasn't been updated yet!</h2>
                            </div>
                        </div>
                        <div v-else>
                            <b-modal id="bv-modal-description" hide-footer>
                                <template #modal-title>
                                    Update Profile Description
                                </template>
                                <div class="d-block text-center">
                                    <b-form-input v-model="descriptionUpdateText"
                                        placeholder="Enter description "></b-form-input>
                                </div>
                                <div class="d-flex">
                                    <b-button class="mt-3 mr-3" variant="success" @click="updateProfileDescription"
                                        :disabled="!validateDescriptionUpdate" block>Update Profile</b-button>
                                    <b-button class="mt-3" block variant="danger"
                                        @click="$bvModal.hide('bv-modal-description')">Cancel</b-button>
                                </div>
                            </b-modal>
                            <b-skeleton v-if="loading"></b-skeleton>
                            <p v-if="!loading && userProfile.description != null" style="text-align: left">{{
                                userProfile.description }}<span class="ml-2"><b-icon-pen-fill
                                        @click="$bvModal.show('bv-modal-description')"></b-icon-pen-fill></span></p>
                            <b-button @click="$bvModal.show('bv-modal-description')"
                                v-if="!loading && userProfile.description === null">Add Description</b-button>
                            <div class="about-cards">
                                <div v-if="loading">
                                    <b-skeleton-img no-aspect height="100px" width="310px"
                                        style="border-radius: 5px"></b-skeleton-img>
                                </div>
                                <div v-if="loading">
                                    <b-skeleton-img no-aspect height="100px" width="310px"
                                        style="border-radius: 5px"></b-skeleton-img>
                                </div>
                                <div v-if="loading">
                                    <b-skeleton-img no-aspect height="100px" width="310px"
                                        style="border-radius: 5px"></b-skeleton-img>
                                </div>

                                <b-modal id="bv-modal-location" hide-footer>
                                    <template #modal-title>
                                        Update Location
                                    </template>
                                    <div class="d-block text-center">
                                        <div class="d-flex">
                                            <h6 class="m-0 mr-1">Lives in</h6>
                                            <b-form-input v-model="locationUpdateText"
                                                placeholder="Enter Location "></b-form-input>
                                        </div>
                                    </div>
                                    <div class="d-flex">
                                        <b-button @click="updateProfileLocation" class="mt-3 mr-3" variant="success"
                                            :disabled="!validateLocationUpdate" block>Update Profile</b-button>
                                        <b-button class="mt-3" block variant="danger"
                                            @click="$bvModal.hide('bv-modal-location')">Cancel</b-button>
                                    </div>
                                </b-modal>

                                <div v-if="!loading && userProfile.current_location != null" class="about-card">
                                    <b-icon-geo-alt-fill class="mr-2"></b-icon-geo-alt-fill>
                                    <div class="location-text">
                                        <p>Lives in <b>{{ userProfile.current_location }}</b></p>
                                    </div>
                                </div>

                                <div v-if="!loading && userProfile.current_location === null" class="about-card">
                                    <b-icon-plus-circle @click="$bvModal.show('bv-modal-location')"
                                        @mouseover="isLocationHovering = true" @mouseleave="isLocationHovering = false"
                                        :class="{ hovering: isLocationHovering }" font-scale="2"
                                        class="mr-2"></b-icon-plus-circle>
                                    <div class="location-text">
                                        <p>Add Location</p>
                                    </div>
                                </div>

                                <b-modal id="bv-modal-profession" hide-footer>
                                    <template #modal-title>
                                        Update Profession
                                    </template>
                                    <div class="d-block text-center">
                                        <div class="d-flex">
                                            <b-form-input v-model="professionUpdateText"
                                                placeholder="Enter profession "></b-form-input>
                                            <p class="m-0 mr-1 ml-1">at</p>
                                            <b-form-input v-model="companyUpdateText"
                                                placeholder="Enter company "></b-form-input>
                                        </div>
                                    </div>
                                    <div class="d-flex">
                                        <b-button @click="updateProfileProfession" class="mt-3 mr-3" variant="success"
                                            :disabled="!validateProfessionUpdate" block>Update Profile</b-button>
                                        <b-button class="mt-3" block variant="danger"
                                            @click="$bvModal.hide('bv-modal-profession')">Cancel</b-button>
                                    </div>
                                </b-modal>

                                <div v-if="!loading && userProfile.profession != null" class="about-card">
                                    <b-icon-briefcase class="mr-2"></b-icon-briefcase>
                                    <div class="location-text">
                                        <p>{{ userProfile.profession }} at <b>{{ userProfile.current_company }}</b></p>
                                    </div>
                                </div>

                                <div v-if="!loading && userProfile.profession === null" class="about-card">
                                    <b-icon-plus-circle @click="$bvModal.show('bv-modal-profession')"
                                        @mouseover="isProfessionHovering = true" @mouseleave="isProfessionHovering = false"
                                        :class="{ hovering: isProfessionHovering }" font-scale="2"
                                        class="mr-2"></b-icon-plus-circle>
                                    <div class="location-text">
                                        <p>Add Profession</p>
                                    </div>
                                </div>

                                <b-modal id="bv-modal-social" hide-footer>
                                    <template #modal-title>
                                        Update Profile Description
                                    </template>
                                    <div class="d-block text-center">
                                        <b-form-input v-model="socialUpdateText"
                                            placeholder="Enter social link"></b-form-input>
                                    </div>
                                    <div class="d-flex">
                                        <b-button @click="updateProfileSocial" class="mt-3 mr-3" variant="success"
                                            :disabled="!validateSocialUpdate" block>Update Profile</b-button>
                                        <b-button class="mt-3" block variant="danger"
                                            @click="$bvModal.hide('bv-modal-social')">Cancel</b-button>
                                    </div>
                                </b-modal>

                                <div v-if="!loading && userProfile.primary_link != null" class="about-card">
                                    <b-icon-person class="mr-2"></b-icon-person>
                                    <div class="location-text">
                                        <p><b>{{ userProfile.primary_link }}</b></p>
                                    </div>
                                </div>

                                <div v-if="!loading && userProfile.primary_link === null" class="about-card">
                                    <b-icon-plus-circle @click="$bvModal.show('bv-modal-social')"
                                        @mouseover="isSocialHovering = true" @mouseleave="isSocialHovering = false"
                                        :class="{ hovering: isSocialHovering }" font-scale="2"
                                        class="mr-2"></b-icon-plus-circle>
                                    <div class="location-text">
                                        <p>Add Social Link</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </b-tab>
                <b-tab :disabled="!isFollowing && !isCurrentUser">
                    <template v-slot:title>
                        <b-icon-newspaper class="mr-2"></b-icon-newspaper>
                        <span>Blogs ({{ blogs.length }})</span>
                    </template>
                    <b-row class="d-flex justify-content-start">
                        <div v-for="(blog, index) in blogs" :key="index" style="width: 30%; margin-right: 3%">
                            <profile-blog-card @delete-blog="deleteBlog" :blogDetails="blog"></profile-blog-card>
                        </div>
                    </b-row>
                </b-tab>
            </b-tabs>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import ProfileBlogCard from '../ProfileBlogCard.vue';

export default {
    components: { ProfileBlogCard },
    props: {
        userDetails: {
            required: true
        },
        isUser: {
            required: true
        }
    },
    data() {
        return {
            userProfile: {
                description: null,
                current_location: null,
                profession: null,
                current_company: null,
                primary_link: null,
            },
            loading: true,
            isRequestSent: false,
            isFollowing: false,
            isLocationHovering: false,
            isProfessionHovering: false,
            isSocialHovering: false,
            descriptionUpdateText: '',
            locationUpdateText: '',
            professionUpdateText: '',
            socialUpdateText: '',
            isCurrentUser: false,
            companyUpdateText: '',
            blogs: [],
            cards: [
                {
                    title: "Ann Venensa",
                    text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut libero sed purus rutrum dapibus. Proin condimentum lobortis mauris, vel aliquet mauris varius at.",
                    imageUrl: "https://via.placeholder.com/75x75",
                },
                {
                    title: "Lina Mars",
                    text: "Nullam quis aliquam elit, ac sagittis sapien. Integer in hendrerit orci. Nulla facilisi. Praesent a lectus at quam lacinia sollicitudin. In hac habitasse platea dictumst.",
                    imageUrl: "https://via.placeholder.com/75x75",
                },
                {
                    title: "John Doe",
                    text: "Suspendisse vel ante id nisl pharetra venenatis. Duis vel diam eget velit consequat pulvinar. Donec in erat vel sem blandit laoreet eu quis velit.",
                    imageUrl: "https://via.placeholder.com/75x75",
                },
                {
                    title: "Jade Smith",
                    text: "Nam commodo vestibulum risus, at scelerisque augue varius ac. Sed eget ligula vel enim finibus tincidunt. Aenean eget eros eu ipsum efficitur eleifend.",
                    imageUrl: "https://via.placeholder.com/75x75",
                },
                {
                    title: "Johanna Watson",
                    text: "Aliquam vestibulum ligula nec velit ullamcorper posuere. Curabitur vitae enim lectus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.",
                    imageUrl: "https://via.placeholder.com/75x75",
                },
            ]

        }
    },
    methods: {
        async sendFollowRequest() {
            await axios({
                method: 'post',
                url: 'http://localhost:5000/api/v1/follow',
                data: {
                    sender_id: localStorage.getItem('user_id'),
                    receiver_id: this.userDetails.u_id
                },
                // headers: {
                //     'x-access-token': localStorage.getItem('token')
                // }
            }).then((response) => {
                if (response.data.success == true) {
                    this.isRequestSent = true;
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
        deleteFollowRequest() {
            axios({
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
        updateProfileDescription() {
            var formData = new FormData();
            formData.append('description', this.descriptionUpdateText);
            formData.append('current_location', this.userProfile.current_location);
            formData.append('profession', this.userProfile.profession);
            formData.append('current_company', this.userProfile.current_company);
            formData.append('primary_link', this.userProfile.primary_link);

            axios({
                method: 'post',
                url: 'http://localhost:5000/api/v1/user-profile',
                data: formData,
                headers: {
                    'x-access-token': localStorage.getItem('token'),
                    'Content-Type': 'multipart/form-data'
                }
            }).then((response) => {
                if (response.data.success == false) {
                    this.loading = false;
                }
                else {
                    this.userProfile.description = response.data.user_profile.description;
                    this.userProfile.current_location = response.data.user_profile.current_location;
                    this.userProfile.profession = response.data.user_profile.profession;
                    this.userProfile.current_company = response.data.user_profile.current_company;
                    this.userProfile.primary_link = response.data.user_profile.primary_link;
                    this.descriptionUpdateText = '';
                    this.$bvModal.hide('bv-modal-description');
                    this.$bvToast.toast('Profile description updated successfully', {
                        title: 'Profile Description Updated',
                        variant: 'success',
                        solid: true,
                        autoHideDelay: 1000
                    })
                }
            })
        },

        updateProfileLocation() {
            var formData = new FormData();
            formData.append('current_location', this.locationUpdateText);
            formData.append('description', this.userProfile.description);
            formData.append('profession', this.userProfile.profession);
            formData.append('current_company', this.userProfile.current_company);
            formData.append('primary_link', this.userProfile.primary_link);


            axios({
                method: 'post',
                url: 'http://localhost:5000/api/v1/user-profile',
                data: formData,
                headers: {
                    'x-access-token': localStorage.getItem('token'),
                    'Content-Type': 'multipart/form-data'
                }
            }).then((response) => {
                if (response.data.success == false) {
                    this.loading = false;
                }
                else {
                    this.userProfile.description = response.data.user_profile.description;
                    this.userProfile.current_location = response.data.user_profile.current_location;
                    this.userProfile.profession = response.data.user_profile.profession;
                    this.userProfile.current_company = response.data.user_profile.current_company;
                    this.userProfile.primary_link = response.data.user_profile.primary_link;
                    this.locationUpdateText = '';
                    this.$bvModal.hide('bv-modal-location');
                    this.$bvToast.toast('Profile location updated successfully', {
                        title: 'Profile Location Updated',
                        variant: 'success',
                        solid: true,
                        autoHideDelay: 1000
                    })
                }
            })
        },

        updateProfileProfession() {
            var formData = new FormData();
            formData.append('profession', this.professionUpdateText);
            formData.append('current_company', this.companyUpdateText);
            formData.append('description', this.userProfile.description);
            formData.append('current_location', this.userProfile.current_location);
            formData.append('primary_link', this.userProfile.primary_link);


            axios({
                method: 'post',
                url: 'http://localhost:5000/api/v1/user-profile',
                data: formData,
                headers: {
                    'x-access-token': localStorage.getItem('token'),
                    'Content-Type': 'multipart/form-data'
                }
            }).then((response) => {
                if (response.data.success == false) {
                    this.loading = false;
                }
                else {
                    this.userProfile.description = response.data.user_profile.description;
                    this.userProfile.current_location = response.data.user_profile.current_location;
                    this.userProfile.profession = response.data.user_profile.profession;
                    this.userProfile.current_company = response.data.user_profile.current_company;
                    this.userProfile.primary_link = response.data.user_profile.primary_link;
                    this.professionUpdateText = '';
                    this.companyUpdateText = '';
                    this.$bvModal.hide('bv-modal-profession');
                    this.$bvToast.toast('Profile profession updated successfully', {
                        title: 'Profile Profession Updated',
                        variant: 'success',
                        solid: true,
                        autoHideDelay: 1000
                    })
                }
            })
        },

        updateProfileSocial() {
            var formData = new FormData();
            formData.append('primary_link', this.socialUpdateText);
            formData.append('profession', this.userProfile.profession);
            formData.append('current_company', this.userProfile.current_company);
            formData.append('description', this.userProfile.description);
            formData.append('current_location', this.userProfile.current_location);


            axios({
                method: 'post',
                url: 'http://localhost:5000/api/v1/user-profile',
                data: formData,
                headers: {
                    'x-access-token': localStorage.getItem('token'),
                    'Content-Type': 'multipart/form-data'
                }
            }).then((response) => {
                if (response.data.success == false) {
                    this.loading = false;
                }
                else {
                    this.userProfile.description = response.data.user_profile.description;
                    this.userProfile.current_location = response.data.user_profile.current_location;
                    this.userProfile.profession = response.data.user_profile.profession;
                    this.userProfile.current_company = response.data.user_profile.current_company;
                    this.userProfile.primary_link = response.data.user_profile.primary_link;
                    this.socialUpdateText = '';
                    this.$bvModal.hide('bv-modal-social');
                    this.$bvToast.toast('Profile Social Links updated successfully', {
                        title: 'Profile Social Links Updated',
                        variant: 'success',
                        solid: true,
                        autoHideDelay: 1000
                    })
                }
            })
        },
        async getFollowRequests() {
            await axios(
                {
                    method: 'get',
                    url: 'http://localhost:5000/api/v1/follow-requests/' + this.userDetails.u_id,

                }
            ).then((response) => {
                response.data.map((item) => {
                    if (item.sender_id == localStorage.getItem('user_id')) {
                        this.isRequestSent = true;
                    }
                })
            }).catch((error) => {
                console.log(error);
            })
        },

        async getCurrentUserProfile() {
            await axios.get('http://localhost:5000/api/v1/user-profile', {
                headers: {
                    'x-access-token': localStorage.getItem('token')
                }
            }).then((response) => {
                if (response.data.success == false) {
                    this.loading = false;
                }
                else {
                    this.userProfile.description = response.data.user_profile.description;
                    this.userProfile.current_location = response.data.user_profile.current_location;
                    this.userProfile.profession = response.data.user_profile.profession;
                    this.userProfile.current_company = response.data.user_profile.current_company;
                    this.userProfile.primary_link = response.data.user_profile.primary_link;
                    this.loading = false;
                }
            }).catch((error) => {
                console.log(error);
            })
        },

        async getUserProfile() {
            await axios.get(`http://localhost:5000/api/v1/user-profile/${this.userDetails.u_id}`, {
                headers: {
                    'x-access-token': localStorage.getItem('token')
                }
            }).then((response) => {
                console.log("From any user profile:", response.data)
                if (response.data.success == false) {
                    this.loading = false;
                }
                else {
                    this.userProfile.description = response.data.user_profile.description;
                    this.userProfile.current_location = response.data.user_profile.current_location;
                    this.userProfile.profession = response.data.user_profile.profession;
                    this.userProfile.current_company = response.data.user_profile.current_company;
                    this.userProfile.primary_link = response.data.user_profile.primary_link;
                    this.loading = false;
                }
            }).catch((error) => {
                console.log(error);
            })
        },

        async checkIfFollowing() {
            await axios.get(`http://localhost:5000/api/v1/is-following/${this.$store.state.user_id}/${this.userDetails.u_id}`).then((response) => {
                if (response.data.success == true) {
                    this.isFollowing = true;
                }
            }).catch((error) => {
                console.log(error);
            })
        },

        async unfollowUser() {
            await axios.delete(`http://localhost:5000/api/v1/unfollow/${this.$store.state.user_id}/${this.userDetails.u_id}`).then((response) => {
                if (response.data.success == true) {
                    this.isFollowing = false;
                }
            }).catch((error) => {
                console.log(error);
            })
        },

        async getAllBlogs() {
            await axios.get(`http://localhost:5000/api/v1/user-blogs/${this.userDetails.u_id}`, {
                headers: {
                    'x-access-token': localStorage.getItem('token')
                }
            }).then((response) => {
                this.blogs = response.data.blogs;
            }).catch((error) => {
                console.log(error);
            })
        },

        deleteBlog(blog_id) {
            this.blogs = this.blogs.filter((item) => {
                return item.blog_id != blog_id;
            })
        },
    },
    computed: {
        validateDescriptionUpdate() {
            return this.descriptionUpdateText.length > 7 ? true : false;
        },
        validateLocationUpdate() {
            return this.locationUpdateText.length > 2 ? true : false;
        },
        validateProfessionUpdate() {
            return this.professionUpdateText.length > 2 && this.companyUpdateText.length > 3 ? true : false;
        },
        validateSocialUpdate() {
            return this.socialUpdateText.length > 5 ? true : false;
        },
        isProfileVisible() {
            // console.log("From Computed:" ,this.isCurrentUser)
            return !this.isFollowing && !this.isCurrentUser;
        }
    },
    watch: {
        userDetails: async function () {
            if (localStorage.getItem('user_id') == +this.userDetails.u_id) {
                this.isCurrentUser = true
                await this.getCurrentUserProfile();
            }
            else {
                this.isCurrentUser = false
                await this.getUserProfile();
            }
            this.getFollowRequests();
            this.checkIfFollowing();
            this.getAllBlogs();
        },
    }
}
</script>

<style scoped>
.header-card {
    position: relative;
    width: 100%;
    background-color: #fff;
    padding-top: 55px;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
}

.hovering {
    cursor: pointer;
    transform: scale(1.1);
}

.profile-cover {
    width: 100%;
    height: 20rem;
}

.profile-image {
    position: absolute;
    top: 19rem;
    left: 2rem;
}

.profile-details {
    margin-top: 10%;
}

.profile-name {
    margin: 0 0 0 2rem;
    text-align: left;
}

.profile-name h3 {
    margin: 0;
}

.profile-bio {
    margin: 0.5rem 0 0 2rem;
    text-align: left;
}

.tabs-container {
    margin: 0 0 0 2rem;
}

.about-cards {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin: 1rem 0;
}

.about-card {
    display: flex;
    align-items: center;
    margin: 0.5rem 0;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    width: 30%;
    padding: 1.5rem 1rem;
    border-radius: 0.5rem;
}

.location-text {
    text-align: left;
}

.location-text p {
    margin: 0;
}

.friends-search {
    justify-content: center;
}

.my-scrollable-cards-container {
    display: flex;
    flex-direction: column;
    max-height: 300px;
    overflow-y: scroll;
    align-items: center;
}

.my-scrollable-cards-container::-webkit-scrollbar {
    width: 0.3em;
}

.my-scrollable-cards-container::-webkit-scrollbar-track {
    background-color: #f5f5f5;
}

.my-scrollable-cards-container::-webkit-scrollbar-thumb {
    background-color: #000000;
    border-radius: 50px;
}

.friends-card {
    display: flex;
    align-items: center;
    margin: 0.1rem 0;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    width: 100%;
    padding: 0.3rem 1rem;
    border-radius: 0.5rem;
    text-align: left;
}

.profile-follow-button {
    margin-right: 5%;
}
</style>