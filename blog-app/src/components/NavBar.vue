<template>
    <b-navbar toggleable="lg" type="light" class="custom-navbar" variant="light">
        <b-navbar-brand href="/dashboard"><i>Scribble Sphere</i></b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>

            <!-- <b-nav-form class="ml-auto">
                <b-input-group prepend="@">
                    <b-form-input placeholder="Username"></b-form-input>
                </b-input-group>
            </b-nav-form> -->

            <!-- Right aligned nav items -->
            <b-navbar-nav class="ml-auto">
                <b-nav-item-dropdown right>
                    <!-- Using 'button-content' slot -->
                    <template #button-content>
                        <em>@{{ username }}</em>
                    </template>
                    <b-dropdown-item><router-link :to="'/profile/' + user_id" >Profile</router-link></b-dropdown-item>
                    <b-dropdown-item @click="signOutClick">Sign Out</b-dropdown-item>
                </b-nav-item-dropdown>
            </b-navbar-nav>
        </b-collapse>
    </b-navbar>
</template>

<script>
import { mapActions } from 'vuex';
export default {
    name: "NavBar",
    props: {
        username: {
            required: true
        },
        user_id: {
            required: true
        }
    },
    data() {
        return {
     
        }
    },
    methods: {
        ...mapActions({
            signOut: 'LOGOUT_ACTION'
        }),
        signOutClick() {
            this.signOut()
        }
    },
}
</script>

<style scoped>
.custom-navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 999;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    width: 100%;
}
</style>