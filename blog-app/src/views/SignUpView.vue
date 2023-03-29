<template>
    <b-container class="base-container">
        <b-row style="justify-content: center; padding-top: 150px">
            <b-col cols="6">
                <div class="form-container">
                    <h1>Create Your Account</h1>
                    <b-form style="width: 80%;" @submit="onSubmit" @reset="onReset">
                        <b-form-group id="email-group" label="Email address:" label-for="email"
                            description="We'll never share your email with anyone else.">
                            <b-input-group>
                                <b-form-input autocomplete="off" :state="emailState" id="email" v-model="form.email"
                                    type="email" placeholder="Enter your email" required></b-form-input>
                                <b-form-invalid-feedback id="input-live-feedback">
                                    Invalid Email
                                </b-form-invalid-feedback>
                                <template #prepend>
                                    <b-input-group-text>
                                        <b-icon-envelope></b-icon-envelope>
                                    </b-input-group-text>
                                </template>
                            </b-input-group>
                        </b-form-group>
                        <div class="d-flex">

                            <b-form-group class="mr-3" id="name-group" label="First Name:" label-for="first-name">
                                <b-form-input autocomplete="off" :state="firstNameState" id="first-name" type="text"
                                    v-model="form.firstName" placeholder="First name" trim required></b-form-input>
                                <b-form-invalid-feedback id="input-live-feedback">
                                    First Name should contain atleast 3 characters
                                </b-form-invalid-feedback>
                            </b-form-group>

                            <b-form-group id="name-group" label="Last Name:" label-for="username">
                                <b-form-input id="last-name" v-model="form.lastName" placeholder="Last name"
                                    required></b-form-input>
                            </b-form-group>

                        </div>

                        <b-input-group class="mt-1 mb-3" prepend="@" id="username-group">
                            <b-form-input id="username" v-model="form.username" placeholder="Username"
                                required></b-form-input>
                        </b-input-group>

                        <b-form-group id="bio-group" label="Bio:" label-for="bio">
                            <b-form-input id="bio" v-model="form.bio" :state="bioState" type="text"
                                placeholder="Enter your bio" maxlength="50" required></b-form-input>
                            <b-form-invalid-feedback id="input-live-feedback">
                                Bio should be atleast a minimum of 10 characters long and a maximum of 50 characters
                            </b-form-invalid-feedback>
                            <b-form-text id="input-live-help">Character count: {{ bioLengthRemaining }}/50</b-form-text>
                        </b-form-group>

                        <b-button type="submit" variant="primary">Submit</b-button>
                    </b-form>
                </div>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
export default {
    data() {
        return {
            form: {
                email: '',
                firstName: '',
                lastName: '',
                username: '',
                bio: '',
            },
        }
    },
    methods: {
        validateEmail(email) {
            const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            return re.test(email)

        },
        onSubmit(event) {
            event.preventDefault()
            alert(JSON.stringify(this.form))
            this.$router.push('/dashboard')
        },
        onReset(event) {
            event.preventDefault()
            // Reset our form values
            this.form.email = ''
            this.form.firstName = ''
            this.form.lastName = ''
            this.form.username = ''
            this.form.bio = ''
        }
    },
    computed: {
        emailState() {
            return this.validateEmail(this.form.email) ? true : false
        },
        firstNameState() {
            return this.form.firstName.length > 2 ? true : false
        },
        bioState() {
            return this.form.bio.length < 51 && this.form.bio.length > 9 ? true : false
        },
        bioLengthRemaining() {
            return this.form.bio.length
        }
    }
}
</script>

<style>
.base-container {
    height: 100vh;
}

.form-container {
    width: 100%;
    text-align: left;
    margin-top: 5%;
    background-color: #fff;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    padding: 5%;
    border-radius: 2%;
}
</style>