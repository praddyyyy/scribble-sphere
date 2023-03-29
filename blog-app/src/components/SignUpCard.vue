<template>
    <div class="form-container" style="margin-top: 15px">
        <h1>Create Your Account</h1>
        <b-form @submit="onSubmit" @reset="onReset">
            <b-form-group id="email-group" label="Email address:" label-for="email"
                description="We'll never share your email with anyone else.">
                <b-input-group>
                    <b-form-input autocomplete="off" :state="emailState" id="email" v-model="form.email" type="email"
                        @blur="blurEmailInput" placeholder="Enter your email" required></b-form-input>
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
                <b-form-group class="mr-3" id="name-group" label="First Name:" label-for="first-name"
                    :state="firstNameState">
                    <b-form-input autocomplete="off" :state="firstNameState" id="first-name" type="text"
                        v-model="form.firstName" @blur="blurfirstNameInput" placeholder="First name" trim
                        required></b-form-input>
                    <b-form-invalid-feedback id="input-live-feedback">
                        First Name should contain atleast 3 characters
                    </b-form-invalid-feedback>
                </b-form-group>

                <b-form-group id="name-group" label="Last Name:" label-for="username">
                    <b-form-input id="last-name" v-model="form.lastName" placeholder="Last name" required></b-form-input>
                </b-form-group>

            </div>

            <b-input-group class="mt-1 mb-3" prepend="@" id="username-group">
                <b-form-input id="username" v-model="form.username" placeholder="Username" required></b-form-input>
            </b-input-group>

            <b-form-group id="password-group" label="Password:" label-for="password">
                <b-input-group class="mt-0">
                    <template #prepend>
                        <b-input-group-text>
                            <b-icon-key></b-icon-key>
                        </b-input-group-text>
                    </template>
                    <b-form-input :state="passwordState" :type="showPassword ? 'text' : 'password'" id="password"
                        @focus="focusPasswordInput" @blur="blurPasswordInput" v-model="form.password" placeholder="Password"
                        required></b-form-input>
                    <template #append>
                        <b-button :variant="!showPassword ? 'primary' : 'danger'" @click="showPassword = !showPassword">
                            <b-icon :icon="!showPassword ? 'eye-slash' : 'eye'"></b-icon>
                        </b-button>
                    </template>
                </b-input-group>
                <div v-if="showPasswordValidators" class="d-flex justify-content-between mt-2">
                    <div class="d-flex align-items-center">
                        <b-icon-patch-check-fill :variant="passwordLength ? 'success' : 'danger'"></b-icon-patch-check-fill>
                        <p class="m-0 ml-1">6 Characters</p>
                    </div>
                    <div class="d-flex align-items-center">
                        <b-icon-patch-check-fill
                            :variant="passwordUpperCase ? 'success' : 'danger'"></b-icon-patch-check-fill>
                        <p class="m-0 ml-1">1 Uppercase</p>
                    </div>
                    <div class="d-flex align-items-center">
                        <b-icon-patch-check-fill
                            :variant="passwordLowerCase ? 'success' : 'danger'"></b-icon-patch-check-fill>
                        <p class="m-0 ml-1">1 Lowercase</p>
                    </div>
                    <div class="d-flex align-items-center">
                        <b-icon-patch-check-fill :variant="passwordNumber ? 'success' : 'danger'"></b-icon-patch-check-fill>
                        <p class="m-0 ml-1">1 Number</p>
                    </div>
                    <div class="d-flex align-items-center">
                        <b-icon-patch-check-fill
                            :variant="passwordSpecial ? 'success' : 'danger'"></b-icon-patch-check-fill>
                        <p class="m-0 ml-1">1 Special</p>
                    </div>
                </div>
            </b-form-group>

            <b-form-group id="confirm-password-group" label="Confirm Password:" label-for="confirm-password">
                <b-input-group class="mt-0">
                    <template #prepend>
                        <b-input-group-text>
                            <b-icon-key></b-icon-key>
                        </b-input-group-text>
                    </template>
                    <b-form-input :state="confirmPasswordState" :type="showConfirmPassword ? 'text' : 'password'"
                        id="confirm-password" v-model="form.confirmPassword" placeholder="Confirm Password"
                        required></b-form-input>
                    <template #append>
                        <b-button :variant="!showConfirmPassword ? 'primary' : 'danger'"
                            @click="showConfirmPassword = !showConfirmPassword">
                            <b-icon :icon="!showConfirmPassword ? 'eye-slash' : 'eye'"></b-icon>
                        </b-button>
                    </template>
                </b-input-group>
            </b-form-group>

            <b-form-group id="bio-group" label="Bio:" label-for="bio">
                <b-form-input autocomplete="off" id="bio" v-model="form.bio" :state="bioState" type="text"
                    @blur="blurBioInput" placeholder="Enter your bio" maxlength="50" required></b-form-input>
                <b-form-invalid-feedback id="input-live-feedback">
                    Bio should be atleast a minimum of 10 characters long and a maximum of 50 characters
                </b-form-invalid-feedback>
                <b-form-text id="input-live-help">Character count: {{ bioLengthRemaining }}/50</b-form-text>
            </b-form-group>
            <p>Already have an account? <a @click="$emit('login-account')">Login</a></p>
            <b-button type="submit" variant="primary">Create Account</b-button>
        </b-form>
    </div>
</template>

<script>
// import axios from 'axios';
import { mapActions } from 'vuex';
export default {
    data() {
        return {
            form: {
                email: '',
                firstName: '',
                lastName: '',
                username: '',
                password: '',
                confirmPassword: '',
                bio: '',
            },
            showPassword: false,
            showConfirmPassword: false,
            showPasswordValidators: false,
            firstNameState: null,
            emailState: null,
            passwordState: null,
            bioState: null,
            invalidFeedback: "Please enter between 2 to 50 characters.",
        }
    },
    watch: {
        "form.firstName": function (val) {
            if (val.length > 2) {
                this.firstNameState = true
            } else {
                this.firstNameState = false
            }
        },
        "form.email": function () {
            if (this.validateEmail(this.form.email)) {
                this.emailState = true
            } else {
                this.emailState = false
            }
        },
        "form.password": function () {
            if (this.validatePassword(this.form.password)) {
                this.passwordState = true
            } else {
                this.passwordState = false
            }
        },
        "form.bio": function () {
            if (this.form.bio.length < 51 && this.form.bio.length > 9) {
                this.bioState = true
            } else {
                this.bioState = false
            }
        }
    },
    methods: {
        ...mapActions({
            signup: 'SIGNUP_ACTION'
        }),
        blurfirstNameInput() {
            if (this.firstNameState === false) {
                this.firstNameState = false
            } else {
                this.firstNameState = null
            }
        },
        blurEmailInput() {
            if (this.emailState === false) {
                this.emailState = false
            } else {
                this.emailState = null
            }
        },
        blurPasswordInput() {
            if (this.passwordState === false) {
                this.passwordState = false
            } else {
                this.passwordState = null
                this.showPasswordValidators = false
            }
        },
        blurBioInput() {
            if (this.bioState === false) {
                this.bioState = false
            } else {
                this.bioState = null
            }
        },

        focusPasswordInput() {
            this.showPasswordValidators = true
        },
        validateEmail(email) {
            const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            return re.test(email)

        },
        validatePassword(password) {
            const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/
            return re.test(password)
        },
        onSubmit(event) {
            event.preventDefault()
            // const path = 'http://localhost:5000/api/v1/signup';

            var formData = new FormData();
            formData.append('firstName', this.form.firstName)
            formData.append('lastName', this.form.lastName)
            formData.append('email', this.form.email)
            formData.append('username', this.form.username)
            formData.append('bio', this.form.bio)
            formData.append('password', this.form.password)
            formData.append('cPassword', this.form.confirmPassword)

            this.signup(formData)
            // axios({
            //     method: 'post',
            //     url: path,
            //     data: formData,
            //     headers: { 'Content-Type': 'multipart/form-data' }
            // })
            //     .then((res) => {
            //         this.msg = res.data;
            //         console.log("API Result: ", this.msg)
            //         if (res.status === 200) {
            //             // this.$router.push('/dashboard')
            //             console.log('first')
            //         }
            //     })
            //     .catch((error) => {
            //         // eslint-disable-next-line
            //         console.error(error);
            //     });
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
        bioLengthRemaining() {
            return this.form.bio.length
        },
        passwordLength() {
            return this.form.password.length > 5 ? true : false
        },
        passwordUpperCase() {
            return /[A-Z]/.test(this.form.password) ? true : false
        },
        passwordLowerCase() {
            return /[a-z]/.test(this.form.password) ? true : false
        },
        passwordNumber() {
            return /[0-9]/.test(this.form.password) ? true : false
        },
        passwordSpecial() {
            return /[!@#$%^&*()]/.test(this.form.password) ? true : false
        },
        confirmPasswordState() {
            if (this.form.confirmPassword.length === 0) {
                return null
            }
            return this.form.password === this.form.confirmPassword ? true : false
        },

    },
}
</script>

<style>
.form-container {
    width: 100%;
    text-align: left;
    background-color: #fff;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    border-radius: 2%;
}
</style>