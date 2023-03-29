<template>
    <b-container fluid class="base-container">
        <b-row class="h-100">
            <b-col cols="1">
            </b-col>
            <b-col cols="6">
                <b-container class="heading-container">
                    <div style="text-align: left; padding-top: 50%">
                        <h1>Scribble Sphere</h1>
                        <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Doloribus sed quasi ipsam tempora!
                            Asperiores alias labore iste odit natus voluptas amet animi inventore, beatae, doloribus
                            deserunt accusamus ipsam enim iusto!</p>
                    </div>
                </b-container>
            </b-col>
            <b-col cols="4">
                <!-- <div class="form-container">
                    <h1>Login to your Account</h1>
                    <b-form style="width: 70%" @submit="onSubmit" @reset="onReset">
                        <b-form-group id="username-group" label="Username:" label-for="username">
                            <b-input-group class="mt-0">
                                <template #prepend>
                                    <b-input-group-text>
                                        <b-icon-envelope></b-icon-envelope>
                                    </b-input-group-text>
                                </template>
                                <b-form-input id="username" v-model="form.username" placeholder="Username"
                                    required></b-form-input>
                            </b-input-group>
                        </b-form-group>

                        <b-form-group id="password-group" label="Password:" label-for="password">
                            <b-input-group class="mt-0">
                                <template #prepend>
                                    <b-input-group-text>
                                        <b-icon-key></b-icon-key>
                                    </b-input-group-text>
                                </template>
                                <b-form-input :type="showPassword ? 'text' : 'password'" id="password"
                                    v-model="form.password" placeholder="Password" required></b-form-input>
                                <template #append>
                                    <b-button :variant="!showPassword ? 'primary' : 'danger'"
                                        @click="showPassword = !showPassword">
                                        <b-icon :icon="!showPassword ? 'eye-slash' : 'eye'"></b-icon>
                                    </b-button>
                                </template>
                            </b-input-group>
                        </b-form-group>

                        <b-form-group id="input-group-4" v-slot="{ ariaDescribedby }">
                            <b-form-checkbox-group v-model="form.checked" id="checkboxes-4"
                                :aria-describedby="ariaDescribedby">
                                <b-form-checkbox value="remember">Remember Me</b-form-checkbox>
                            </b-form-checkbox-group>
                        </b-form-group>
                        <p style="margin: 2% 0">Don't have an account? <a href="/signup">Create one</a></p>

                        <b-button type="submit" variant="primary">Login</b-button>
                    </b-form>
                </div> -->
                <login-card v-if="showLogin" @create-account="showLogin = false"></login-card>
                <sign-up-card v-else @login-account="showLogin = true"></sign-up-card>
            </b-col>
            <b-col cols="1">
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import LoginCard from '../components/LoginCard.vue'
import SignUpCard from '../components/SignUpCard.vue'
export default {
    components: { LoginCard, SignUpCard },
    data() {
        return {
            form: {
                username: '',
                password: '',
                checked: [],
            },
            showPassword: false,
            showLogin: true
        }
    },
    methods: {
        onSubmit(event) {
            event.preventDefault()
            alert(JSON.stringify(this.form))
            this.$router.push('/dashboard')
        },
        onReset(event) {
            event.preventDefault()
            // Reset our form values
            this.form.email = ''
            this.form.username = ''
            this.form.checked = []
        }
    }
}
</script>

<style scoped>
.base-container {
    height: 100vh;
}

.heading-container {
    height: 100%;
    width: 70%;
}

.form-container {
    text-align: left;
    margin-top: 35%;
    background-color: #fff;
    box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
    padding: 10% 5%;
    border-radius: 5%;
}
</style>